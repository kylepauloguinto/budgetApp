from datetime import date, datetime, timedelta
import calendar
from typing import Tuple
from django.utils import timezone
from django.db.models import Sum
from .models import Account, Schedule

# -------------------------
# Helper date utilities
# -------------------------
def _is_last_day_of_month(d: date) -> bool:
    return d.day == calendar.monthrange(d.year, d.month)[1]

def _add_months(d: date, months: int) -> date:
    """Add months to a date while preserving last-day-of-month behavior."""
    m = d.month - 1 + months
    y = d.year + m // 12
    m = m % 12 + 1
    day = min(d.day, calendar.monthrange(y, m)[1])
    return date(y, m, day)

def _add_years(d: date, years: int) -> date:
    """Add years while preserving last-day-of-month behavior (Feb29 -> Feb28 if needed)."""
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        # Feb 29 -> Feb 28 on non-leap years
        return date(d.year + years, d.month, calendar.monthrange(d.year + years, d.month)[1])

def _months_diff(start: date, later: date) -> int:
    return (later.year - start.year) * 12 + (later.month - start.month)

def occurrences_between_by_days(start_date: date, interval_days: int, range_start: date, range_end: date) -> int:
    """
    Count occurrences of events happening every `interval_days` starting from `start_date`,
    but only those that fall within [range_start, range_end].
    
    Rule A:
    - No extra +1 if start_date is before the range.
    - Pure floor division based on valid occurrences inside range.
    """
    s = start_date
    if range_end < start_date:
        return 0

    # first possible occurrence index k such that occurrence_date >= range_start
    if range_start <= start_date:
        k0 = 0
    else:
        k0 = 0
        k1Start_date = start_date
        while k1Start_date < range_start:
            k0 += 1
            k1Start_date += timedelta(days=interval_days)

    first = start_date + timedelta(days=k0 * interval_days)
    if first > range_end:
        return 0
    # last possible occurrence index k such that occurrence_date <= range_end
    k1 = 0
    while start_date <= range_end:
        k1 += 1
        start_date += timedelta(days=interval_days)
    
    return max(0, k1 - k0)

def occurrences_between_by_months(start_date: date, every_n_months: int, range_start: date, range_end: date) -> int:
    """
    Count occurrences where occ_k = start_date + k*every_n_months months and occ_k in [range_start, range_end].
    """
    if range_end < start_date:
        return 0
    count = 0
    k = 0
    while True:
        occ = _add_months(start_date, k * every_n_months)
        if occ > range_end:
            break
        if occ >= range_start:
            count += 1
        k += 1
    return count

def occurrences_between_by_years(start_date: date, every_n_years: int, range_start: date, range_end: date) -> int:
    if range_end < start_date:
        return 0
    count = 0
    k = 0
    while True:
        occ = _add_years(start_date, k * every_n_years)
        if occ > range_end:
            break
        if occ >= range_start:
            count += 1
        k += 1
    return count

# -------------------------
# Utilities: schedule date extraction
# -------------------------
def get_schedule_start_date(schedule) -> date:
    """Support common field names for schedule start datetime and return a date object."""
    dt = None
    name = 'startScheduleDate'
    if hasattr(schedule, name):
        dt = getattr(schedule, name)
    if dt is None:
        # fallback to "ins_date" or similar
        dt = getattr(schedule, 'ins_date', None)
    if dt is None:
        raise ValueError("Schedule has no start datetime field recognized (expected startScheduleDate).")
    if isinstance(dt, datetime):
        return dt.date()
    if isinstance(dt, date):
        return dt
    # if string
    try:
        return datetime.fromisoformat(str(dt)).date()
    except Exception:
        raise ValueError("Cannot parse schedule start date: %r" % (dt,))

# -------------------------
# Main functions
# -------------------------
def _get_current_total(account: Account) -> float:
    """
    Prefer latest account.balance or sum of applied schedule amounts.
    """
    # account.balance if exists
    if hasattr(account, 'balance'):
        try:
            return float(account.balance)
        except Exception:
            pass
    return float(0.0)

def _earliest_schedule_year_for_account(account: Account) -> int:
    schedules = Schedule.objects.filter(accountNameSchedule=account).order_by('startScheduleDate')
    if not schedules.exists():
        # fallback to current year if no schedules
        return timezone.now().year
    # get earliest date_start
    first = schedules.first()
    start = get_schedule_start_date(first)
    return start.year

def _yearly_total_for_schedule(schedule, year: int) -> float:
    """
    Compute total amount contributed by a SINGLE schedule in a given calendar year (year).
    """
    start_date = get_schedule_start_date(schedule)

    amt = float(schedule.amount)
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)
    if schedule.recurrence == 'once':
        if start_date >= year_start and start_date <= year_end:
            return amt
        return 0.0
    if schedule.recurrence == 'daily':
        occ = occurrences_between_by_days(start_date, schedule.periodCountSchedule, max(start_date, year_start), year_end)
        return occ * amt
    if schedule.recurrence == 'weekly':
        occ = occurrences_between_by_days(start_date, 7 * schedule.periodCountSchedule, max(start_date, year_start), year_end)
        return occ * amt
    if schedule.recurrence == 'monthly':
        occ = occurrences_between_by_months(start_date, schedule.periodCountSchedule, max(start_date, year_start), year_end)
        return occ * amt
    if schedule.recurrence == 'yearly':
        occ = occurrences_between_by_years(start_date, schedule.periodCountSchedule, max(start_date, year_start), year_end)
        return occ * amt
    return 0.0

def _monthly_total_for_schedule_in_month(schedule, year: int, month: int) -> float:
    """Compute total amount added by schedule during the given month (month start..month end inclusive)."""
    start_date = get_schedule_start_date(schedule)
    
    amt = float(schedule.amount)
    month_start = date(year, month, 1)
    month_end = date(year, month, calendar.monthrange(year, month)[1])
    # Do not count occurrences before start_date in the same month
    effective_start = max(start_date, month_start)
    if schedule.recurrence == 'once':
        return amt if (start_date >= month_start and start_date <= month_end) else 0.0
    if schedule.recurrence == 'daily':
        if month_end < start_date:
            return 0.0
        occ = occurrences_between_by_days(start_date, schedule.periodCountSchedule, effective_start, month_end)
        return occ * amt
    if schedule.recurrence == 'weekly':
        # every N weeks where N>1: use exact landing occurrences (7*k days interval)
        if month_end < start_date:
            return 0.0
        occ = occurrences_between_by_days(start_date, 7 * schedule.periodCountSchedule, effective_start, month_end)
        return occ * amt
    if schedule.recurrence == 'monthly':
        if month_end < start_date:
            return 0.0
        # Count occurrences of start_date + n*k months that fall inside [effective_start, month_end]
        occ = occurrences_between_by_months(start_date, schedule.periodCountSchedule, effective_start, month_end)
        return occ * amt
    if schedule.recurrence == 'yearly':
        if month_end < start_date:
            return 0.0
        occ = occurrences_between_by_years(start_date, schedule.periodCountSchedule, effective_start, month_end)
        return occ * amt
    return 0.0

# -------------------------
# Main API
# -------------------------
def predict_future_income(user, account_id: int, target_year: int) -> dict:
    """
    Main function should call.
    Behavior:
        - Start from earliest schedule year for account (Start Year: A).
        - base_balance = current account total (IncomeHistory/account.balance)
        - For each year in [start_year .. target_year-1], compute all incomes and add to base_balance.
        - Then compute month-end cumulative balances for target_year and return only that year's months.
    """
    account = Account.objects.get(id=account_id,
                                    userAccount=user)
    schedules = list(Schedule.objects.filter(accountNameSchedule=account))

    transfer_debit_schedules = list(Schedule.objects.filter(accountNameScheduleTransferTo_id=account_id))
    transfer_credit_schedules = list(Schedule.objects.filter(accountNameScheduleTransferFrom_id=account_id))

    # base_current is canonical current total
    base_current = _get_current_total(account)
    account_date = account.ins_date

    if schedules:
        # Determine start year from earliest schedule start
        earliest = min(get_schedule_start_date(s) for s in schedules)
        start_year = earliest.year
    else:
        start_year = timezone.now().year

    # 1) Accumulate full-year totals from start_year up to target_year-1
    base_balance = float(base_current)
    for y in range(start_year, target_year):
        year_sum = 0.0
        for s in schedules:
            year_total = _yearly_total_for_schedule(s, y)
            if s.scheduleType == "debit":
                year_sum += year_total
            elif s.scheduleType == "credit":
                year_sum -= year_total
        for s in transfer_debit_schedules:
            year_sum += _yearly_total_for_schedule(s, y)
        for s in transfer_credit_schedules:
            year_sum -= _yearly_total_for_schedule(s, y)
        base_balance += year_sum

    # keep the value for response (in case want to display previous year balance)
    entering_balance = round(base_balance, 2)

    # 2) Compute month-end cumulative balances for target_year only
    result_months = []
    running = 0.0
    if account_date.year < target_year:
        running = base_balance
    for m in range(1, 13):
        if account_date.year == target_year and m == account_date.month:
            running += base_balance

        month_add = 0.0
        for s in schedules:
            monthly_total = _monthly_total_for_schedule_in_month(s, target_year, m)
            if s.scheduleType == "debit":
                month_add += monthly_total
            elif s.scheduleType == "credit":
                month_add -= monthly_total
        for s in transfer_debit_schedules:
            month_add += _monthly_total_for_schedule_in_month(s, target_year, m)
        for s in transfer_credit_schedules:
            month_add -= _monthly_total_for_schedule_in_month(s, target_year, m)

        running += month_add
        result_months.append({
            "month": m,
            "date": calendar.month_abbr[m],
            "predicted_total": round(running, 2),
            "added_this_month": round(month_add, 2)
        })

    return result_months

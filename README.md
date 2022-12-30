# Budget Tracker webapp

## CS50
>This was my final project for conclude the CS50 Introduction to Computer Science course.
>CS, python, JavaScript, bootstrap web development, CS50

## Why did I build this project?
Having a bad habit of spending leads us to unsuccessful life. Over spending makes us poor and unstable future. Not knowing where our money goes is not advisable and makes us feel anxious. That is why it is better to track and put your expenses and income into something place to helps us to know where our money goes. And I am proud to introduce the Budget Tracker app. By tracking our expenses, we can manage our money and helps us if we are on the stage of overspending it. It reminds us when and where to stop and most especially helps us to motivate to save money. Seeing your money flow by progress bar or graphs helps a lot to build good habit of spending. This application can help us to know where our money goes and track it. 

## How the webpage works?
My project is a website that tracks your budget by registering a `transactions`. In the account section, it displays all the transactions of every bank accounts. The transactions can be also edited and delete. To track the transactions, The user can `create`, `edit` and `delete` `budgets`. In this section, the user can set amount limits and tracks the transactions within certain period of time, category or subcategory and which bank account it will be track. Every transaction will reflect in set budgets. Once the certain period has reached, it will be automatically reset the next end period and amount of spent to zero. The user can also see the transactions within certain period of set time by clicking the item and click `transactions`. In the `schedule` section, the user can `create`, `edit` and `delete` schedules. The schedule section is for automatically registration of a transaction in set date and time. Once it registered, it will no longer display if it is not set to `repeat`. In order to make use of the tracking every transaction, the `report` section displays expenses and income in graph by year, account and category or subcategory. It will also show every transaction depends on the search conditions by month by clicking it. 

## How to use Budget Tracker 
1. The first to thing do is to create an account. 
2. And then, the user can create unlimited number of bank accounts to track. It can also be edited and delete.
3. lastly, create categories and subcategories. It can also be edited and delete. There is no limit in certain number of categories and subcategories.

Once you have created a bank account and categories or subcategories, you can now create a transaction.

#### Tips
* Use budget screen to track the budget of certain amount limit.
* You can use schedule screen to automatically make a transaction in set date and time.
* Look for the reports for monthly transactions. 

### How to add transaction
By clicking the `plus button` on main screen or inside the bank account screen, it will send you to add transaction screen.

### How to edit transaction
Inside the bank account screen, click the transaction item, the dropdown will display and click `edit`. It will send you to edit transaction screen.

### How to delete transaction
Inside the bank account screen, click the transaction item, the dropdown will display and click `delete`. It will send you to edit transaction screen.

## Application structure

- Login screen: Login your account by putting your username and password
- All accounts screen (It will display if more than 1 bank account was created): Displays all transactions of all accounts
- (Created bank account) screen: Display the transactions of certain bank account
- Budget screen: Display the expenses on what item you are tracking as a progress bar
- Schedule screen: Displays the scheduled transaction
- Reports screen: Displays the expenses and income by graph
- Settings screen: The place where you can create an account and categories or subcategories

#### Files & Directories

- `Main Directory`

  - `budgetApp` - Main application directory.
    - `static` - Holds all static files.
      - `css` - Contain all css files for styling the website.
      - `index.js` - Contains all JavaScript files for manipulating the DOM with ajax functionalities.
      - `logo.png` - Logo of the application.
    - `Templates` - Holds all html files.
    - `models.py` - Contains eight classes User, Account, Categories, Subcategories, Transaction, Budget, Schedule and Report which has all information about Application.
    - `urls.py` - Contains all url paths for Account, Categories, Subcategories, Transaction, Budget, Schedule, Settings and Report. Like display, add, edit and delete Account, Categories, Subcategories, Transaction, Budget, Schedule and Report.
    - `views.py` - Contains all view functions for Account, Categories, Subcategories, Transaction, Budget, Schedule, Settings and Report (mentioned in `urls.py`).

## About this application
Making an application that is different to previous web application project is very challenging. It takes a lot of time and effort to think of what application should i make. By thinking of what i need and a tool that can help me in my daily life, I came up to this application. Building from scratch is not an easy task. But while I'm building this application, endless ideas are coming up. What makes this application differ to previous project is that it is all about tracking your money by displaying it by progress bar and graphs. Because it is all about numbers, making it sure that the amount registered, edited and deleted transaction that should reflect to created Budget and graphs in report page is what makes this application complex. The amount should not be more or less to other screens and making sure it is properly reflected and has an equal amount. Building this application helps me to learn more and the complexity of this application is what i really enjoy. And this application is also full mobile responsive support.

## How to run the application
1. Clone the code: `git clone https://github.com/guintokylep/budgetApp.git`
2. Install project dependencies by running `pip install --user django`
3. Run command prompt in the folder and run `python manage.py makemigrations` and `python manage.py migrate`.
4. Once installed run command `python manage.py runserver`
5. In your browser go to `localhost:80000`
6. You are ready to go!

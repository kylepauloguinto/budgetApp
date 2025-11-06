document.addEventListener("DOMContentLoaded", function () {
  url = window.location.href;
  path = url.split("/")[3];
  id = url.split("/")[4];
  
  if (path === "predictions") {
    searchPredictionsIncome();

    $("#year").on("change", function () {
      searchPredictionsIncome();
    });

    $("#accountName-report").on("change", function () {
      searchPredictionsIncome();
    });

    $("#category").on("change", function () {
      searchPredictionsIncome();
    });

    $("#subCategory").on("change", function () {
      searchPredictionsIncome();
    });
  }

})

function searchPredictionsIncome() {
  const ctx = document.getElementById("myChart").getContext("2d");
  let year = $("#year").val();
  let accountName = $("#accountName-report").val();
  let data = {
    year: year,
    accountName: accountName,
  };
  expenses = "";
  income = "";
  fetch("predictions/predictionsDisplay", {
    method: "POST",
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((report) => {
      date = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ];
      let data = {
        labels: date,
        datasets: [
          {
            label: " Income ",
            data: report.values,
            borderColor: "rgb(60, 186, 113,0.7)",
            backgroundColor: "rgb(60, 186, 113,0.7)",
          },
        ],
      };
      let barOptions = {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      };

      if (myChart != null) {
        myChart.destroy();
      }
      myChart = new Chart(ctx, {
        type: "line",
        data: data,
        options: barOptions,
      });

      myChart.update();
      let mainDiv = document.getElementById("dates");
      mainDiv.innerHTML = "";
      // report.months.forEach((data) => {
      //   let monthName = "";
      //   if (data == 1) {
      //     monthName = "January";
      //   } else if (data == 2) {
      //     monthName = "February";
      //   } else if (data == 3) {
      //     monthName = "March";
      //   } else if (data == 4) {
      //     monthName = "April";
      //   } else if (data == 5) {
      //     monthName = "May";
      //   } else if (data == 6) {
      //     monthName = "June";
      //   } else if (data == 7) {
      //     monthName = "July";
      //   } else if (data == 8) {
      //     monthName = "August";
      //   } else if (data == 9) {
      //     monthName = "September";
      //   } else if (data == 10) {
      //     monthName = "October";
      //   } else if (data == 11) {
      //     monthName = "November";
      //   } else if (data == 12) {
      //     monthName = "December";
      //   }
      //   // transaction information
      //   const main = document.createElement("div");
      //   main.setAttribute("class", "dropright");
      //   main.setAttribute("style", "margin-bottom: 10px;");
      //   const a = document.createElement("a");
      //   a.setAttribute(
      //     "class",
      //     `list-group-item list-group-item-action inbx-clck fs-2`
      //   );
      //   a.setAttribute("href", "#");
      //   a.setAttribute("id", "dropdownMenuLink");
      //   a.setAttribute("role", "button");
      //   a.setAttribute("data-toggle", "dropdown");
      //   a.setAttribute("aria-haspopup", "true");
      //   a.setAttribute("aria-expanded", "false");
      //   a.setAttribute("data-bs-toggle", "modal");
      //   a.setAttribute("data-bs-target", "#modalReport");
      //   a.setAttribute(
      //     "onClick",
      //     `reportDisplay(${data},${year},${accountName},${category},'${subcategory}')`
      //   );

      //   // transaction description
      //   let divRow1 = document.createElement("div");
      //   divRow1.setAttribute("class", "row");
      //   let divRow1Col1 = document.createElement("div");
      //   divRow1Col1.setAttribute("class", "col");
      //   divRow1Col1.setAttribute("style", "text-align: left;");

      //   let divRowLabel1 = document.createElement("label");
      //   divRowLabel1.innerHTML = monthName;
      //   divRow1Col1.append(divRowLabel1);
      //   divRow1.append(divRow1Col1);
      //   a.append(divRow1);

      //   main.append(a);
      //   mainDiv.append(main);
      // });
    });
}

function reportDisplay(month, year, accountName, category, subcategory) {
  let monthData = month;
  let yearData = year;
  let accountNameData = accountName;
  let categoryData = category;
  let subcategoryData = subcategory;
  let data = {
    month: monthData,
    year: yearData,
    accountName: accountNameData,
    category: categoryData,
    subcategory: subcategoryData,
  };

  let monthName = "";
  if (month == 1) {
    monthName = "January";
  } else if (month == 2) {
    monthName = "February";
  } else if (month == 3) {
    monthName = "March";
  } else if (month == 4) {
    monthName = "April";
  } else if (month == 5) {
    monthName = "May";
  } else if (month == 6) {
    monthName = "June";
  } else if (month == 7) {
    monthName = "July";
  } else if (month == 8) {
    monthName = "August";
  } else if (month == 9) {
    monthName = "September";
  } else if (month == 10) {
    monthName = "October";
  } else if (month == 11) {
    monthName = "November";
  } else if (month == 12) {
    monthName = "December";
  }

  let title = document.getElementById("reportTitle");
  title.innerHTML = monthName + " " + year;

  let income = document.getElementById("reportIncome");
  income.innerHTML = "";
  let expenses = document.getElementById("reportExpenses");
  expenses.innerHTML = "";

  fetch("predictions/predictionsDetail", {
    method: "POST",
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((transaction) => {
      transaction.forEach((data) => {
        // transaction information
        const main = document.createElement("div");
        main.setAttribute("class", "dropright");
        const a = document.createElement("a");
        a.setAttribute(
          "class",
          `list-group-item list-group-item-action inbx-clck fs-2 ${data.id}`
        );
        a.setAttribute("href", "#");
        a.setAttribute("id", "dropdownMenuLink");
        a.setAttribute("role", "button");
        a.setAttribute("data-toggle", "dropdown");
        a.setAttribute("aria-haspopup", "true");
        a.setAttribute("aria-expanded", "false");

        // transaction description
        let divRow1 = document.createElement("div");
        divRow1.setAttribute("class", "row");
        let divRow1Col1 = document.createElement("div");
        divRow1Col1.setAttribute("class", "col");
        divRow1Col1.setAttribute("style", "text-align: left;");
        let divRow1Col2 = document.createElement("div");
        divRow1Col2.setAttribute("class", "col");
        divRow1Col2.setAttribute("style", "text-align: right;");

        let divRowLabel1 = document.createElement("label");
        divRowLabel1.setAttribute("style", "font-size: 15px;");
        divRowLabel1.innerHTML = data.descriptionTransaction;
        divRow1Col1.append(divRowLabel1);
        divRow1.append(divRow1Col1);

        // transfer information
        let divRow2 = document.createElement("div");
        divRow2.setAttribute("class", "row");
        let divCol1 = document.createElement("div");
        let divCol2 = document.createElement("div");
        let divCol3 = document.createElement("div");
        let divColLabel1 = document.createElement("label");
        let divColLabel2 = document.createElement("label");
        let divColLabel3 = document.createElement("label");
        divColLabel1.setAttribute("style", "font-size: 16px;");
        divColLabel1.innerHTML = data.transactionDate;
        divCol1.setAttribute("class", "col");
        divCol1.append(divColLabel1);
        divRow2.append(divCol1);

        // amount and icon
        divCol3.setAttribute("class", "col");
        divCol3.setAttribute("style", "text-align: right;");
        let i = document.createElement("i");
        let iYen = document.createElement("i");
        iYen.setAttribute("class", "bi bi-currency-yen");
        if (data.transactionType === "credit") {
          i.setAttribute("class", "bi bi-dash-circle");
          i.setAttribute("style", "color: red");
        } else if (data.transactionType === "debit") {
          i.setAttribute("class", "bi bi-plus-circle");
          i.setAttribute("style", "color: rgb(46, 180, 46)");
        } else if (id != "0") {
          if (data.accountNameTransferFromId == id) {
            i.setAttribute("class", "bi bi-dash-circle");
            i.setAttribute("style", "color: red");
          } else if (data.accountNameTransferToId == id) {
            i.setAttribute("class", "bi bi-plus-circle");
            i.setAttribute("style", "color: rgb(46, 180, 46)");
          }
        }
        divColLabel3.append(i);
        divColLabel3.append(iYen);
        divColLabel3.append(data.amount);
        divCol3.append(divColLabel3);
        divRow2.append(divCol3);
        a.append(divRow1);
        a.append(divRow2);

        main.append(a);

        if (data.transactionType == "credit") {
          expenses.append(main);
        } else if (data.transactionType == "debit") {
          income.append(main);
        }
      });
    });
}


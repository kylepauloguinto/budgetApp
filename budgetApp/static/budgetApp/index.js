let TRANSACTION_CODE = "";
let url = "";
let path = "";
let id = "";
let transaction_edit_id = ""
document.addEventListener("DOMContentLoaded", function () {
    

    url = window.location.href
    path = url.split("/")[3]
    id = url.split("/")[4]

    // category credit pulldown changed in add and edit transaction
    $( "#category" ).change(function() {
        let parentValue = this.value;

        $( "#category-debit" ).val(parentValue);

        if( parentValue != ""){
            // credit section
            $("#subCategory").val('').trigger('change');
            document.getElementById("subCategory").removeAttribute("hidden");
            document.getElementById("label-sub").removeAttribute("hidden");

            let option = document.getElementById("subCategory").options.length;
            let subCategory =  document.getElementById("subCategory");
            let hiddentCount = 0;

            for(let i = 0 ; i < option ; i++){
                let value = subCategory.options[i].value ;
                value = value.split("-")
                if(parentValue != value[0]){
                    hiddentCount++;
                    subCategory.options[i].setAttribute("hidden", "hidden");
                    document.getElementById("label-sub").setAttribute("hidden", "hidden");
                }else{
                    subCategory.options[i].removeAttribute("hidden");
                    document.getElementById("label-sub").removeAttribute("hidden");
                }
            }
            if(option == hiddentCount){
                document.getElementById("subCategory").setAttribute("hidden", "hidden");
                document.getElementById("label-sub").setAttribute("hidden", "hidden");
            }
            
            // debit section
            $("#subCategory-debit").val('').trigger('change');
            document.getElementById("subCategory-debit").removeAttribute("hidden");
            document.getElementById("label-sub-debit").removeAttribute("hidden");

            option = document.getElementById("subCategory-debit").options.length;
            subCategory =  document.getElementById("subCategory-debit");
            hiddentCount = 0;

            for(let i = 0 ; i < option ; i++){
                let value = subCategory.options[i].value ;
                value = value.split("-")
                if(parentValue != value[0]){
                    hiddentCount++;
                    subCategory.options[i].setAttribute("hidden", "hidden");
                    document.getElementById("label-sub-debit").setAttribute("hidden", "hidden");
                }else{
                    subCategory.options[i].removeAttribute("hidden");
                    document.getElementById("label-sub-debit").removeAttribute("hidden");
                }
            }
            if(option == hiddentCount){
                document.getElementById("subCategory-debit").setAttribute("hidden", "hidden");
                document.getElementById("label-sub-debit").setAttribute("hidden", "hidden");
            }
        }else{
            $("#subCategory").val('').trigger('change');
            document.getElementById("subCategory").setAttribute("hidden", "hidden");
            document.getElementById("label-sub").setAttribute("hidden", "hidden");
            
            $("#subCategory-debit").val('').trigger('change');
            document.getElementById("subCategory-debit").setAttribute("hidden", "hidden");
            document.getElementById("label-sub-debit").setAttribute("hidden", "hidden");
        }
    });

    // category debit pulldown changed in add and edit transaction
    $( "#category-debit" ).change(function() {
        let parentValue = this.value;

        $( "#category" ).val(parentValue);

        if( parentValue != ""){
            // debit section
            $("#subCategory-debit").val('').trigger('change');
            document.getElementById("subCategory-debit").removeAttribute("hidden");
            document.getElementById("label-sub-debit").removeAttribute("hidden");

            let option = document.getElementById("subCategory-debit").options.length;
            let subCategory =  document.getElementById("subCategory-debit");
            let hiddentCount = 0;

            for(let i = 0 ; i < option ; i++){
                let value = subCategory.options[i].value ;
                value = value.split("-")
                if(parentValue != value[0]){
                    hiddentCount++;
                    subCategory.options[i].setAttribute("hidden", "hidden");
                    document.getElementById("label-sub-debit").setAttribute("hidden", "hidden");
                }else{
                    subCategory.options[i].removeAttribute("hidden");
                    document.getElementById("label-sub-debit").removeAttribute("hidden");
                }
            }
            if(option == hiddentCount){
                document.getElementById("subCategory-debit").setAttribute("hidden", "hidden");
                document.getElementById("label-sub-debit").setAttribute("hidden", "hidden");
            }

            // credit section
            $("#subCategory").val('').trigger('change');
            document.getElementById("subCategory").removeAttribute("hidden");
            document.getElementById("label-sub").removeAttribute("hidden");
 
            option = document.getElementById("subCategory").options.length;
            subCategory =  document.getElementById("subCategory");
            hiddentCount = 0;
 
            for(let i = 0 ; i < option ; i++){
                let value = subCategory.options[i].value ;
                value = value.split("-")
                if(parentValue != value[0]){
                    hiddentCount++;
                    subCategory.options[i].setAttribute("hidden", "hidden");
                    document.getElementById("label-sub").setAttribute("hidden", "hidden");
                }else{
                    subCategory.options[i].removeAttribute("hidden");
                    document.getElementById("label-sub").removeAttribute("hidden");
                }
            }
            if(option == hiddentCount){
                document.getElementById("subCategory").setAttribute("hidden", "hidden");
                document.getElementById("label-sub").setAttribute("hidden", "hidden");
            }
        }else{
            $("#subCategory").val('').trigger('change');
            document.getElementById("subCategory").setAttribute("hidden", "hidden");
            document.getElementById("label-sub").setAttribute("hidden", "hidden");

            $("#subCategory-debit").val('').trigger('change');
            document.getElementById("subCategory-debit").setAttribute("hidden", "hidden");
            document.getElementById("label-sub-debit").setAttribute("hidden", "hidden");
        }
    });

    // origin account has change in transfer section
    $( "#accountNameFrom" ).change(function() {
        let accountNameFrom = this.value;
            $("#accountNameTo").val('').trigger('change');
            let option = document.getElementById("accountNameTo").options.length;
        let accountNameTo =  document.getElementById("accountNameTo");
            for(let i = 0 ; i < option ; i++){
            let value = accountNameTo.options[i].value ;
            value = value.split("-")
            if(accountNameFrom == value[0]){
                accountNameTo.options[i].setAttribute("hidden", "hidden");
            }else if(accountNameTo.options[i].value == ""){
                accountNameTo.options[i].setAttribute("hidden", "hidden");
            }else{
                accountNameTo.options[i].removeAttribute("hidden");
            }
        }

        $("#accountName-credit").val(this.value);
        $("#accountName-debit").val(this.value);
    });

    // add transaction section
    if( path == 'addTransaction'){
        // Set previous screen link
        let previousScreen = sessionStorage.getItem("previousScreen");
        if( previousScreen === "index"){
            $("#backAdd").attr('href','/');
        }else{
            $("#backAdd").attr('href',`/display/${previousScreen}`);
        }

        // when page of add transaction loads, set transaction code as credit
        TRANSACTION_CODE = "credit";

        $("#pills-credit-tab").click(function() {
            TRANSACTION_CODE = "credit";
        })
        $("#pills-debit-tab").click(function() {
            TRANSACTION_CODE = "debit";
        })        
        $( "#pills-transfer-tab" ).click(function() {
            TRANSACTION_CODE = "transfer";
            let accountNameFrom =  document.getElementById("accountNameFrom").value ;

            $("#accountNameTo").val('').trigger('change');

            let option = document.getElementById("accountNameTo").options.length;
            let accountNameTo =  document.getElementById("accountNameTo");

            for(let i = 0 ; i < option ; i++){
                let value = accountNameTo.options[i].value ;
                value = value.split("-")
                if(accountNameFrom == value[0]){
                    accountNameTo.options[i].setAttribute("hidden", "hidden");
                }else{
                    accountNameTo.options[i].removeAttribute("hidden");
                }
            }
        });
    }
   
    if( id == 'editTransaction' ){

        // Set previous screen link
        let previousScreen = sessionStorage.getItem("previousScreen");
        $("#backAdd").attr('href',`/display/${previousScreen}`);

        $("#pills-credit-tab").click(function() {
            TRANSACTION_CODE = "credit";
        })
        $("#pills-debit-tab").click(function() {
            TRANSACTION_CODE = "debit";
        })         
        $( "#pills-transfer-tab" ).click(function() {
            TRANSACTION_CODE = "transfer";
        })
        
        var active_tab = $(".active");
        TRANSACTION_CODE = active_tab.attr('id').split("-")[1]
        transaction_edit_id = url.split("/")[5]

        // credit subCategory function
        let category = document.getElementById("category").value ;
        if (category != "") document.getElementById("subCategory").removeAttribute("hidden");

        let option = document.getElementById("subCategory").options.length;
        let subCategory = document.getElementById("subCategory");
        let hiddentCount = TRANSACTION_CODE == "transfer" ? 1 : 0;
        for(let i = 0 ; i < option ; i++){
            let value = subCategory.options[i].value ;
            value = value.split("-")
            if(category != value[0]){
                hiddentCount++;
                subCategory.options[i].setAttribute("hidden", "hidden");
            }else{
                subCategory.options[i].removeAttribute("hidden");
            }
        }
        if(option == hiddentCount){
            document.getElementById("subCategory").setAttribute("hidden", "hidden");
        }

        // debit subCategory function
        category = document.getElementById("category-debit").value ;
        if (category != "") document.getElementById("subCategory-debit").removeAttribute("hidden");

        option = document.getElementById("subCategory-debit").options.length;
        subCategory = document.getElementById("subCategory-debit");
        hiddentCount = TRANSACTION_CODE == "transfer" ? 1 : 0;

        for(let i = 0 ; i < option ; i++){
            let value = subCategory.options[i].value ;
            value = value.split("-")
            if(category != value[0]){
                hiddentCount++;
                subCategory.options[i].setAttribute("hidden", "hidden");
            }else{
                subCategory.options[i].removeAttribute("hidden");
            }
        }
        if(option == hiddentCount){
            document.getElementById("subCategory-debit").setAttribute("hidden", "hidden");
        }

        // transfer function accountFrom and accountTo 
        let accountNameFrom =  document.getElementById("accountNameFrom").value ;
        option = document.getElementById("accountNameTo").options.length;
        let accountNameTo =  document.getElementById("accountNameTo");

        for(let i = 0 ; i < option ; i++){
            let value = accountNameTo.options[i].value ;
            value = value.split("-")
            if(accountNameFrom == value[0]){
                accountNameTo.options[i].setAttribute("hidden", "hidden");
            }else if(accountNameTo.options[i].value == ""){
                accountNameTo.options[i].setAttribute("hidden", "hidden");
            }else{
                accountNameTo.options[i].removeAttribute("hidden");
            }
        }
    }


    if(path === "display"){
        let pageNo = 1
        $(window).scroll(function() {
            if($(window).scrollTop() + $(window).height() == $(document).height()) {
                pageNo++
                displayPage(id,pageNo)
            }
         });

        // only if in the account transaction section
        if( id != "editTransaction"){
            displayPage(id,pageNo)
        }
    }

    if(path === "budget"){
        fetch('budget/budgetDisplay')
        .then(response => response.json())
        .then(transaction =>{
            let mainDiv = document.getElementById("main");

            transaction.forEach(data => {

                // transaction information
                const main = document.createElement('div');
                main.setAttribute('class','dropright');
                const a = document.createElement('a');
                a.setAttribute('class',`list-group-item list-group-item-action inbx-clck fs-2 ${data.id}`);
                a.setAttribute('href',"#");
                a.setAttribute('id','dropdownMenuLink');
                a.setAttribute('role','button');
                a.setAttribute('data-toggle','dropdown');
                a.setAttribute('aria-haspopup','true');
                a.setAttribute('aria-expanded','false');

                // transaction description
                let divRow0 = document.createElement('div');
                divRow0.setAttribute('class','row');
                let divRow1 = document.createElement('div');
                divRow1.setAttribute('class','row');
                let divRow1Col0 = document.createElement('div');
                divRow1Col0.setAttribute('class','col');
                divRow1Col0.setAttribute('style','text-align: left;');
                let divRow1Col1 = document.createElement('div');
                divRow1Col1.setAttribute('class','col');
                divRow1Col1.setAttribute('style','text-align: left;');
                let divRow1Col2 = document.createElement('div');
                divRow1Col2.setAttribute('class','col');
                divRow1Col2.setAttribute('style','text-align: right;');

                let currentAmount = data.currentAmount.replace(",","")
                let budgetAmount = data.budgetAmount.replace(",","")
                let difference = budgetAmount - currentAmount;

                let divRowLabel0 = document.createElement('label');
                divRowLabel0.setAttribute('style','font-size: 30px;font-weight:bold;');
                divRowLabel0.innerHTML = data.budgetName
                let divRowLabel1 = document.createElement('label');
                divRowLabel1.setAttribute('style','font-size: 25px;');
                divRowLabel1.innerHTML = 'Spent: ¥ ' + data.currentAmount
                let divRowLabel2 = document.createElement('label');
                divRowLabel2.setAttribute('style','font-size: 25px;');
                divRowLabel2.innerHTML = ' ¥ ' + difference
                divRow1Col0.append(divRowLabel0);
                divRow1Col1.append(divRowLabel1);
                divRow1Col2.append(divRowLabel2);
                divRow0.append(divRow1Col0);
                divRow1.append(divRow1Col1);
                divRow1.append(divRow1Col2);

                let percentage = (currentAmount / budgetAmount ) * 100
                let color = ""

                if( percentage <= 100 && percentage >= 80 || data.minusAmount ){
                    color = "bg-danger"
                }else if( percentage < 80 && percentage >= 50 ){
                    color = "bg-warning"
                }else if( percentage < 25 ){
                    color = "bg-info"
                }
                // transfer information
                let divRow2 = document.createElement('div');
                divRow2.setAttribute('class','progress');
                let divColLabel1 = document.createElement('div');
                divColLabel1.setAttribute('class',`progress-bar ${color}`);
                divColLabel1.setAttribute('role','progressbar');
                divColLabel1.setAttribute('aria-label','Basic example');
                divColLabel1.setAttribute('style',`width: ${percentage}%`);
                divColLabel1.setAttribute('aria-valuenow', percentage);
                divColLabel1.setAttribute('aria-valuemin','0');
                divColLabel1.setAttribute('aria-valuemax','100');
                divRow2.append(divColLabel1);

                a.append(divRow0);
                a.append(divRow1);
                a.append(divRow2);

                // notification badge
                if( data.readTransaction == false){
                    const span = document.createElement('span');
                    span.setAttribute('class','position-absolute top-0 start-100 translate-middle p-2 badge rounded-pill bg-danger')
                    span.innerHTML = ' ';
                    a.append(span);
                }

                // dropdown menu
                const divMenu = document.createElement('div');
                divMenu.setAttribute('class','dropdown-menu');
                divMenu.setAttribute('aria-labelledby','dropdownMenuLink');
                const aEdit = document.createElement('a');
                const aDelete = document.createElement('a');
                aEdit.setAttribute('class','dropdown-item');
                aDelete.setAttribute('class','dropdown-item');
                aEdit.setAttribute('href',`editBudget/${data.id}`);
                const iEdit = document.createElement('i');
                const iDelete = document.createElement('i');
                iEdit.setAttribute('class','bi bi-pencil');
                iDelete.setAttribute('class','bi bi-trash3');
                aEdit.append(iEdit);
                aEdit.append(' Edit');
                aEdit.setAttribute('onclick',`edit(${id})`);
                aDelete.append(iDelete);
                aDelete.append(' Delete');
                aDelete.setAttribute('data-bs-toggle','modal');
                aDelete.setAttribute('data-bs-target','#myModal');
                aDelete.setAttribute('onClick',`deleteBudget(${data.id})`);
                aDelete.setAttribute('href','#');
                const divDivider = document.createElement('div');
                divDivider.setAttribute('class','dropdown-divider');
                divMenu.append(aEdit);
                divMenu.append(divDivider);
                divMenu.append(aDelete);

                main.append(a);
                main.append(divMenu);
                mainDiv.append(main);

            });

        })
    }
    if( path == "editBudget"){
        let category = document.getElementById("category").value ;
        if (category != "") document.getElementById("subCategory").removeAttribute("hidden");

        let option = document.getElementById("subCategory").options.length;
        let subCategory = document.getElementById("subCategory");
        let hiddentCount = 0;
        for(let i = 0 ; i < option ; i++){
            let value = subCategory.options[i].value ;
            value = value.split("-")
            if(category != value[0]){
                hiddentCount++;
                subCategory.options[i].setAttribute("hidden", "hidden");
            }else{
                subCategory.options[i].removeAttribute("hidden");
            }
        }
        if(option == hiddentCount){
            document.getElementById("subCategory").setAttribute("hidden", "hidden");
        }
    }
    // Add transaction section event 
    // amount value
    $( "#amount-credit" ).focusout(function() {
        $("#amount-debit").val(this.value);
        $("#amount-transfer").val(this.value);
    });
    
    $( "#amount-debit" ).focusout(function() {
        $("#amount-credit").val(this.value);
        $("#amount-transfer").val(this.value);
    });
    
    $( "#amount-transfer" ).focusout(function() {
        $("#amount-credit").val(this.value);
        $("#amount-debit").val(this.value);
    });
    
    // description value
    $( "#des-credit" ).focusout(function() {
        $("#des-debit").val(this.value);
        $("#des-transfer").val(this.value);
    });
    
    $( "#des-debit" ).focusout(function() {
        $("#des-credit").val(this.value);
        $("#des-transfer").val(this.value);
    });
    
    $( "#des-transfer" ).focusout(function() {
        $("#des-credit").val(this.value);
        $("#des-debit").val(this.value);
    });

    // date value
    $( "#date-credit" ).focusout(function() {
        $("#date-debit").val(this.value);
        $("#date-transfer").val(this.value);
    });
    
    $( "#date-debit" ).focusout(function() {
        $("#date-credit").val(this.value);
        $("#date-transfer").val(this.value);
    });
    
    $( "#date-transfer" ).focusout(function() {
        $("#date-credit").val(this.value);
        $("#date-debit").val(this.value);
    });

    // time value
    $( "#time-credit" ).focusout(function() {
        $("#time-debit").val(this.value);
        $("#time-transfer").val(this.value);
    });
    
    $( "#time-debit" ).focusout(function() {
        $("#time-credit").val(this.value);
        $("#time-transfer").val(this.value);
    });
    
    $( "#time-transfer" ).focusout(function() {
        $("#time-credit").val(this.value);
        $("#time-debit").val(this.value);
    });

    // account name value
    $( "#accountName-credit" ).focusout(function() {
        $("#accountName-debit").val(this.value);
        $("#accountNameFrom").val(this.value);
    });
    
    $( "#accountName-debit" ).focusout(function() {
        $("#accountName-credit").val(this.value);
        $("#accountNameFrom").val(this.value);
    });

    // subcategory value
    $("#subCategory").focusout(function() {
        $("#subCategory-debit").val(this.value);
    })

    $("#subCategory-debit").focusout(function() {
        $("#subCategory").val(this.value);
    })

    // Delete Item
    $("#submitDelete").click(function (){
        let item = $(this).attr("data-id") ;
        let action = $(this).attr("data-action")

        if( action === "transaction") {
            fetch(`/display/${id}/delete`,{
                method: 'POST',
                body: JSON.stringify({item: item })
            })
            .then(response => response.json())
            .then( result => {

                if(result.message == "success" ){
                    // Process for all accounts display
                    if(result.data[0].transactionType === "transfer" && id === "0"){
                        $(`.${result.data[0].id}`).slideUp( "slow", function(){ this.remove(); });
                        $(`.${result.data[0].transactionFromId}`).slideUp( "slow", function(){ this.remove(); });
                    }else{
                        $(`.${item}`).slideUp( "slow", function(){ this.remove(); });
                    }
                    $("#myModal .btn-close").click()
                    let balance = $('.balance').text().replace(',','')
                    let newBalance = result.balance

                    $({ Counter: balance }).animate({
                        Counter: newBalance
                      }, {
                        duration: 1000,
                        easing: 'swing',
                        step: function() {
                          $('.balance').text(Math.ceil(this.Counter));
                        },complete: function(){
                            $('.balance').text(new Intl.NumberFormat('ja-JP').format(newBalance));
                        }
                      });
                }
            })
        }else if(action === "account"){

            fetch("/accounts/delete",{
                method: 'POST',
                body: JSON.stringify({item: item })
            })
            .then(response => response.json())
            .then( result => {

                if(result.message == "success" ){
                    // Process for all accounts display
                    $(`.${item}`).slideUp( "slow", function(){ this.remove(); });
                    $("#myModal .btn-close").click()
                }
            })
        }else if(action === "category"){

            fetch("/categories/deleteCategory",{
                method: 'POST',
                body: JSON.stringify({item: item })
            })
            .then(response => response.json())
            .then( result => {

                if(result.message == "success" ){
                    // Process for all accounts display
                    $(`.${action}-${item}`).slideUp( "slow", function(){ this.remove(); });
                    $("#myModal .btn-close").click()
                }
            })
        }else if(action === "subcategory"){

            fetch("/categories/deleteSubcategory",{
                method: 'POST',
                body: JSON.stringify({item: item })
            })
            .then(response => response.json())
            .then( result => {

                if(result.message == "success" ){
                    // Process for all accounts display
                    $(`.${action}-${item}`).slideUp( "slow", function(){ this.remove(); });
                    $("#myModal .btn-close").click()
                }
            })
        }else if(action === "budget"){

            fetch("/budget/delete",{
                method: 'POST',
                body: JSON.stringify({item: item })
            })
            .then(response => response.json())
            .then( result => {

                if(result.message == "success" ){
                    // Process for all budget display
                    $(`.${item}`).slideUp( "slow", function(){ this.remove(); });
                    $("#myModal .btn-close").click()
                }
            })
        }

    })

});
function displayPage(id,pageNo){
    fetch(`transaction/${id}/${pageNo}`)
        .then(response => response.json())
        .then(transaction =>{
            let mainDiv = document.getElementById("main");

            transaction.forEach(data => {

                // transaction information
                const main = document.createElement('div');
                main.setAttribute('class','dropright');
                const a = document.createElement('a');
                a.setAttribute('class',`list-group-item list-group-item-action inbx-clck fs-2 ${data.id}`);
                a.setAttribute('href',"#");
                a.setAttribute('id','dropdownMenuLink');
                a.setAttribute('role','button');
                a.setAttribute('data-toggle','dropdown');
                a.setAttribute('aria-haspopup','true');
                a.setAttribute('aria-expanded','false');

                // transaction description
                let divRow1 = document.createElement('div');
                divRow1.setAttribute('class','row');
                let divRow1Col1 = document.createElement('div');
                divRow1Col1.setAttribute('class','col');
                divRow1Col1.setAttribute('style','text-align: left;');
                let divRow1Col2 = document.createElement('div');
                divRow1Col2.setAttribute('class','col');
                divRow1Col2.setAttribute('style','text-align: right;');

                let divRowLabel1 = document.createElement('label');
                divRowLabel1.setAttribute('style','font-size: 15px;');
                divRowLabel1.innerHTML = data.accountNameTransaction + ' ¥ ' + data.previousAccountBalance
                let divRowLabel2 = document.createElement('label');
                divRowLabel2.setAttribute('style','font-size: 12px;');
                divRowLabel2.innerHTML = data.transactionDate
                divRow1Col1.append(divRowLabel1);
                divRow1Col2.append(divRowLabel2);
                divRow1.append(divRow1Col1);
                divRow1.append(divRow1Col2);

                // transfer information
                let divRow2 = document.createElement('div');
                divRow2.setAttribute('class','row');
                let divCol1 = document.createElement('div');
                let divCol2 = document.createElement('div');
                let divCol3 = document.createElement('div');
                let divColLabel1 = document.createElement('label');
                let divColLabel2 = document.createElement('label');
                let divColLabel3 = document.createElement('label');
                divColLabel1.innerHTML = data.descriptionTransaction;
                divCol1.setAttribute('class','col');
                divCol1.append(divColLabel1);
                divRow2.append(divCol1);

                divCol2.setAttribute('class','col');
                divCol2.setAttribute('style','text-align: center;');
                if(data.transactionType === 'transfer' && id == 0 ){
                    let i = document.createElement('i');
                    i.setAttribute('class','bi bi-arrow-left-right');
                    divColLabel2.append(data.accountNameTransferFrom);
                    divColLabel2.append(' ');
                    divColLabel2.append(i);
                    divColLabel2.append(' ');
                    divColLabel2.append(data.accountNameTransferTo);
                    divCol2.append(divColLabel2);
                }else{
                    let i = document.createElement('i');
                    if( data.accountNameTransferFromId == id){
                        i.setAttribute('class','bi bi-chevron-bar-up');
                        i.setAttribute('style','color: red');
                        divColLabel2.append(i);
                        divColLabel2.append(data.accountNameTransferTo);
                    }else if ( data.accountNameTransferToId == id ){
                        i.setAttribute('class','bi bi-chevron-bar-down');
                        i.setAttribute('style','color: rgb(46, 180, 46)');
                        divColLabel2.append(i);
                        divColLabel2.append(data.accountNameTransferFrom);
                    }
                    divCol2.append(divColLabel2);
                }
                divRow2.append(divCol2);

                // amount and icon
                divCol3.setAttribute('class','col');
                divCol3.setAttribute('style','text-align: right;');
                let i = document.createElement('i');
                let iYen = document.createElement('i');
                iYen.setAttribute('class','bi bi-currency-yen');
                if(data.transactionType === 'credit'){
                    i.setAttribute('class','bi bi-dash-circle');
                    i.setAttribute('style','color: red');
                }else if(data.transactionType === 'debit'){
                    i.setAttribute('class','bi bi-plus-circle');
                    i.setAttribute('style','color: rgb(46, 180, 46)');
                }else if( id != '0' ){
                    if( data.accountNameTransferFromId == id){
                        i.setAttribute('class','bi bi-dash-circle');
                        i.setAttribute('style','color: red');
                    }else if ( data.accountNameTransferToId == id ){
                        i.setAttribute('class','bi bi-plus-circle');
                        i.setAttribute('style','color: rgb(46, 180, 46)');
                    }
                }
                divColLabel3.append(i);
                divColLabel3.append(iYen);
                divColLabel3.append(data.amount);
                divCol3.append(divColLabel3)
                divRow2.append(divCol3);
                a.append(divRow1);
                a.append(divRow2);

                // notification badge
                if( data.readTransaction == false){
                    const span = document.createElement('span');
                    span.setAttribute('class','position-absolute top-0 start-100 translate-middle p-2 badge rounded-pill bg-danger')
                    span.innerHTML = ' ';
                    a.append(span);
                }

                // dropdown menu
                const divMenu = document.createElement('div');
                divMenu.setAttribute('class','dropdown-menu');
                divMenu.setAttribute('aria-labelledby','dropdownMenuLink');
                const aEdit = document.createElement('a');
                const aDelete = document.createElement('a');
                aEdit.setAttribute('class','dropdown-item');
                aDelete.setAttribute('class','dropdown-item');
                aEdit.setAttribute('href',`editTransaction/${data.id}`);
                const iEdit = document.createElement('i');
                const iDelete = document.createElement('i');
                iEdit.setAttribute('class','bi bi-pencil');
                iDelete.setAttribute('class','bi bi-trash3');
                aEdit.append(iEdit);
                aEdit.append(' Edit');
                aEdit.setAttribute('onclick',`edit(${id})`);
                aDelete.append(iDelete);
                aDelete.append(' Delete');
                aDelete.setAttribute('data-bs-toggle','modal');
                aDelete.setAttribute('data-bs-target','#myModal');
                aDelete.setAttribute('onClick',`deleteItem(${data.id})`);
                aDelete.setAttribute('href','#');
                const divDivider = document.createElement('div');
                divDivider.setAttribute('class','dropdown-divider');
                divMenu.append(aEdit);
                divMenu.append(divDivider);
                divMenu.append(aDelete);

                main.append(a);
                main.append(divMenu);
                mainDiv.append(main);

            });

            fetch(`unread/${id}`)
            .then(response => response.json())
            .then(message =>{
                console.log(message)
            })
        })
}
function addSubmit(){

    if(TRANSACTION_CODE == "credit"){
        let data = {
            amount: $("#amount-credit").val(),
            description: $("#des-credit").val(),
            category: $("#category").val(),
            subcategory: $("#subCategory").val(),
            date: $("#date-credit").val(),
            time: $("#time-credit").val(),
            accountName: $("#accountName-credit").val()
        }

        fetch(`/addTransaction/${id}/creditAdd`,{
            method: 'POST',
            body: JSON.stringify( data )
        })
        .then(response => response.json())
        .then( result => {

            $("#amount-credit").removeClass("is-invalid")
            $("#invalid-amount").html("")
            $("#des-credit").removeClass("is-invalid")
            $("#invalid-des").html("")
            $("#category").removeClass("is-invalid")
            $("#invalid-cat-credit").html("")
            $("#subCategory").removeClass("is-invalid")
            $("#invalid-sub-credit").html("")
            $("#accountName-credit").removeClass("is-invalid")
            $("#invalid-account").html("")
            
            if(result.message == "error" ){
                result.error.forEach(error =>{
                    if( error.id == "amount"){
                        $("#amount-credit").addClass("is-invalid")
                        $("#amount-div").addClass("is-invalid")
                        $("#invalid-amount").html(error.message)
                    }
                    if( error.id == "description"){
                        $("#des-credit").addClass("is-invalid")
                        $("#invalid-des").html(error.message)
                    }
                    if( error.id == "category"){
                        $("#category").addClass("is-invalid")
                        $("#invalid-cat-credit").html(error.message)
                    }
                    if( error.id == "subCategory"){
                        $("#subCategory").addClass("is-invalid")
                        $("#invalid-sub-credit").html(error.message)
                    }
                    if( error.id == "accountName"){
                        $("#accountName-credit").addClass("is-invalid")
                        $("#invalid-account").html(error.message)
                    }
                })
            } else {
                window.location.href = "/";
            }
        })
    }else if(TRANSACTION_CODE == "debit"){
        let data = {
            amount: $("#amount-debit").val(),
            description: $("#des-debit").val(),
            category: $("#category-debit").val(),
            subcategory: $("#subCategory-debit").val(),
            date: $("#date-debit").val(),
            time: $("#time-debit").val(),
            accountName: $("#accountName-debit").val()
        }

        fetch(`/addTransaction/${id}/debitAdd`,{
            method: 'POST',
            body: JSON.stringify( data )
        })
        .then(response => response.json())
        .then( result => {

            $("#amount-debit").removeClass("is-invalid")
            $("#invalid-amount-debit").html("")
            $("#des-debit").removeClass("is-invalid")
            $("#invalid-des-debit").html("")
            $("#category-debit").removeClass("is-invalid")
            $("#invalid-cat-debit").html("")
            $("#subCategory-debit").removeClass("is-invalid")
            $("#invalid-sub-debit").html("")
            $("#accountName-debit").removeClass("is-invalid")
            $("#invalid-account-debit").html("")
            
            if(result.message == "error" ){
                result.error.forEach(error =>{
                    if( error.id == "amount"){
                        $("#amount-debit").addClass("is-invalid")
                        $("#amount-div-debit").addClass("is-invalid")
                        $("#invalid-amount-debit").html(error.message)
                    }
                    if( error.id == "description"){
                        $("#des-debit").addClass("is-invalid")
                        $("#invalid-des-debit").html(error.message)
                    }
                    if( error.id == "category"){
                        $("#category-debit").addClass("is-invalid")
                        $("#invalid-cat-debit").html(error.message)
                    }
                    if( error.id == "subCategory"){
                        $("#subCategory-debit").addClass("is-invalid")
                        $("#invalid-sub-debit").html(error.message)
                    }
                    if( error.id == "accountName"){
                        $("#accountName-debit").addClass("is-invalid")
                        $("#invalid-account-debit").html(error.message)
                    }
                })
            } else {
                window.location.href = "/";
            }
        })
    }else if(TRANSACTION_CODE == "transfer"){
        let data = {
            amount: $("#amount-transfer").val(),
            description: $("#des-transfer").val(),
            date: $("#date-transfer").val(),
            time: $("#time-transfer").val(),
            accountNameFrom: $("#accountNameFrom").val(),
            accountNameTo: $("#accountNameTo").val()
        }

        fetch(`/addTransaction/${id}/transferAdd`,{
            method: 'POST',
            body: JSON.stringify( data )
        })
        .then(response => response.json())
        .then( result => {

            $("#amount-transfer").removeClass("is-invalid")
            $("#invalid-amount-transfer").html("")
            $("#des-transfer").removeClass("is-invalid")
            $("#invalid-des-transfer").html("")
            $("#accountNameFrom").removeClass("is-invalid")
            $("#invalid-account-transfer-from").html("")
            $("#accountNameTo").removeClass("is-invalid")
            $("#invalid-account-transfer-to").html("")
            
            if(result.message == "error" ){
                result.error.forEach(error =>{
                    if( error.id == "amount"){
                        $("#amount-transfer").addClass("is-invalid")
                        $("#amount-div-transfer").addClass("is-invalid")
                        $("#invalid-amount-transfer").html(error.message)
                    }
                    if( error.id == "description"){
                        $("#des-transfer").addClass("is-invalid")
                        $("#invalid-des-transfer").html(error.message)
                    }
                    if( error.id == "accountNameFrom"){
                        $("#accountNameFrom").addClass("is-invalid")
                        $("#invalid-account-transfer-from").html(error.message)
                    }
                    if( error.id == "accountNameTo"){
                        $("#accountNameTo").addClass("is-invalid")
                        $("#invalid-account-transfer-to").html(error.message)
                    }
                })
            } else {
                window.location.href = "/";
            }
        })
    }
};

function editSubmit(){

    if(TRANSACTION_CODE == "credit"){
        let data = {
            amount: $("#amount-credit").val(),
            description: $("#des-credit").val(),
            category: $("#category").val(),
            subcategory: $("#subCategory").val(),
            date: $("#date-credit").val(),
            time: $("#time-credit").val(),
            accountName: $("#accountName-credit").val()
        }

        fetch(`/editTransaction/creditEdit/${transaction_edit_id}`,{
            method: 'POST',
            body: JSON.stringify( data )
        })
        .then(response => response.json())
        .then( result => {

            $("#amount-credit").removeClass("is-invalid")
            $("#invalid-amount").html("")
            $("#des-credit").removeClass("is-invalid")
            $("#invalid-des").html("")
            $("#category").removeClass("is-invalid")
            $("#invalid-cat-credit").html("")
            $("#subCategory").removeClass("is-invalid")
            $("#invalid-sub-credit").html("")
            $("#accountName-credit").removeClass("is-invalid")
            $("#invalid-account").html("")
            
            if(result.message == "error" ){
                result.error.forEach(error =>{
                    if( error.id == "amount"){
                        $("#amount-credit").addClass("is-invalid")
                        $("#amount-div").addClass("is-invalid")
                        $("#invalid-amount").html(error.message)
                    }
                    if( error.id == "description"){
                        $("#des-credit").addClass("is-invalid")
                        $("#invalid-des").html(error.message)
                    }
                    if( error.id == "category"){
                        $("#category").addClass("is-invalid")
                        $("#invalid-cat-credit").html(error.message)
                    }
                    if( error.id == "subCategory"){
                        $("#subCategory").addClass("is-invalid")
                        $("#invalid-sub-credit").html(error.message)
                    }
                    if( error.id == "accountName"){
                        $("#accountName-credit").addClass("is-invalid")
                        $("#invalid-account").html(error.message)
                    }
                })
            } else {
                window.location.href = "/";
            }
        })
    }else if(TRANSACTION_CODE == "debit"){
        let data = {
            amount: $("#amount-debit").val(),
            description: $("#des-debit").val(),
            category: $("#category-debit").val(),
            subcategory: $("#subCategory-debit").val(),
            date: $("#date-debit").val(),
            time: $("#time-debit").val(),
            accountName: $("#accountName-debit").val()
        }

        fetch(`/editTransaction/debitEdit/${transaction_edit_id}`,{
            method: 'POST',
            body: JSON.stringify( data )
        })
        .then(response => response.json())
        .then( result => {

            $("#amount-debit").removeClass("is-invalid")
            $("#invalid-amount-debit").html("")
            $("#des-debit").removeClass("is-invalid")
            $("#invalid-des-debit").html("")
            $("#category-debit").removeClass("is-invalid")
            $("#invalid-cat-debit").html("")
            $("#subCategory-debit").removeClass("is-invalid")
            $("#invalid-sub-debit").html("")
            $("#accountName-debit").removeClass("is-invalid")
            $("#invalid-account-debit").html("")
            
            if(result.message == "error" ){
                result.error.forEach(error =>{
                    if( error.id == "amount"){
                        $("#amount-debit").addClass("is-invalid")
                        $("#amount-div-debit").addClass("is-invalid")
                        $("#invalid-amount-debit").html(error.message)
                    }
                    if( error.id == "description"){
                        $("#des-debit").addClass("is-invalid")
                        $("#invalid-des-debit").html(error.message)
                    }
                    if( error.id == "category"){
                        $("#category-debit").addClass("is-invalid")
                        $("#invalid-cat-debit").html(error.message)
                    }
                    if( error.id == "subCategory"){
                        $("#subCategory-debit").addClass("is-invalid")
                        $("#invalid-sub-debit").html(error.message)
                    }
                    if( error.id == "accountName"){
                        $("#accountName-debit").addClass("is-invalid")
                        $("#invalid-account-debit").html(error.message)
                    }
                })
            } else {
                window.location.href = "/";
            }
        })
    }else if(TRANSACTION_CODE == "transfer"){
        let data = {
            amount: $("#amount-transfer").val(),
            description: $("#des-transfer").val(),
            date: $("#date-transfer").val(),
            time: $("#time-transfer").val(),
            accountNameFrom: $("#accountNameFrom").val(),
            accountNameTo: $("#accountNameTo").val()
        }

        fetch(`/editTransaction/transferEdit/${transaction_edit_id}`,{
            method: 'POST',
            body: JSON.stringify( data )
        })
        .then(response => response.json())
        .then( result => {

            $("#amount-transfer").removeClass("is-invalid")
            $("#invalid-amount-transfer").html("")
            $("#des-transfer").removeClass("is-invalid")
            $("#invalid-des-transfer").html("")
            $("#accountNameFrom").removeClass("is-invalid")
            $("#invalid-account-transfer-from").html("")
            $("#accountNameTo").removeClass("is-invalid")
            $("#invalid-account-transfer-to").html("")
            
            if(result.message == "error" ){
                result.error.forEach(error =>{
                    if( error.id == "amount"){
                        $("#amount-transfer").addClass("is-invalid")
                        $("#amount-div-transfer").addClass("is-invalid")
                        $("#invalid-amount-transfer").html(error.message)
                    }
                    if( error.id == "description"){
                        $("#des-transfer").addClass("is-invalid")
                        $("#invalid-des-transfer").html(error.message)
                    }
                    if( error.id == "accountNameFrom"){
                        $("#accountNameFrom").addClass("is-invalid")
                        $("#invalid-account-transfer-from").html(error.message)
                    }
                    if( error.id == "accountNameTo"){
                        $("#accountNameTo").addClass("is-invalid")
                        $("#invalid-account-transfer-to").html(error.message)
                    }
                })
            } else {
                window.location.href = "/";
            }
        })
    }
};

function deleteItem(id){
    
    $("#submitDelete").attr('data-id',id);
    $("#submitDelete").attr('data-action',"transaction");
    
};

function deleteAccount(id){
    
    $("#submitDelete").attr('data-id',id);
    $("#submitDelete").attr('data-action',"account");
    
};

function deleteCategory(id){
    
    $("#submitDelete").attr('data-id',id);
    $("#submitDelete").attr('data-action',"category");
    
};

function deleteSubcategory(id){
    
    $("#submitDelete").attr('data-id',id);
    $("#submitDelete").attr('data-action',"subcategory");
    
};

function deleteBudget(id){
    
    $("#submitDelete").attr('data-id',id);
    $("#submitDelete").attr('data-action',"budget");
    
};

function edit(id){
    sessionStorage.setItem("previousScreen", id);
}

function addBudget(){
    let data = {
        name: $("#name").val(),
        amount: $("#amount").val(),
        description: $("#des").val(),
        category: $("#category").val(),
        subcategory: $("#subCategory").val(),
        date: $("#date").val(),
        time: $("#time").val(),
        periodCount: $("#periodCount").val(),
        periodProcess: $("#periodProcess").val(),
        accountName: $("#accountName").val()
    }

    fetch('/budgetAdd',{
        method: 'POST',
        body: JSON.stringify( data )
    })
    .then(response => response.json())
    .then( result => {

        $("#name").removeClass("is-invalid")
        $("#invalid-name").html("")
        $("#amount").removeClass("is-invalid")
        $("#invalid-amount").html("")
        $("#des").removeClass("is-invalid")
        $("#invalid-des").html("")
        $("#category").removeClass("is-invalid")
        $("#invalid-cat").html("")
        $("#subCategory").removeClass("is-invalid")
        $("#invalid-sub").html("")
        $("#accountName").removeClass("is-invalid")
        $("#invalid-account").html("")
        
        if(result.message == "error" ){
            result.error.forEach(error =>{
                if( error.id == "name"){
                    $("#name").addClass("is-invalid")
                    $("#invalid-name").html(error.message)
                }
                if( error.id == "amount"){
                    $("#amount").addClass("is-invalid")
                    $("#amount-div").addClass("is-invalid")
                    $("#invalid-amount").html(error.message)
                }
                if( error.id == "description"){
                    $("#des").addClass("is-invalid")
                    $("#invalid-des").html(error.message)
                }
                if( error.id == "category"){
                    $("#category").addClass("is-invalid")
                    $("#invalid-cat").html(error.message)
                }
                if( error.id == "subCategory"){
                    $("#subCategory").addClass("is-invalid")
                    $("#invalid-sub").html(error.message)
                }
                if( error.id == "accountName"){
                    $("#accountName").addClass("is-invalid")
                    $("#invalid-account").html(error.message)
                }
            })
        } else {
            window.location.href = "/budget";
        }
    })
}

function editBudget(){
    let data = {
        name: $("#name").val(),
        amount: $("#amount").val(),
        description: $("#des").val(),
        category: $("#category").val(),
        subcategory: $("#subCategory").val(),
        date: $("#date").val(),
        time: $("#time").val(),
        periodCount: $("#periodCount").val(),
        periodProcess: $("#periodProcess").val(),
        accountName: $("#accountName").val()
    }

    fetch(`/budgetEdit/${id}`,{
        method: 'POST',
        body: JSON.stringify( data )
    })
    .then(response => response.json())
    .then( result => {

        $("#name").removeClass("is-invalid")
        $("#invalid-name").html("")
        $("#amount").removeClass("is-invalid")
        $("#invalid-amount").html("")
        $("#des").removeClass("is-invalid")
        $("#invalid-des").html("")
        $("#category").removeClass("is-invalid")
        $("#invalid-cat").html("")
        $("#subCategory").removeClass("is-invalid")
        $("#invalid-sub").html("")
        $("#accountName").removeClass("is-invalid")
        $("#invalid-account").html("")
        
        if(result.message == "error" ){
            result.error.forEach(error =>{
                if( error.id == "name"){
                    $("#name").addClass("is-invalid")
                    $("#invalid-name").html(error.message)
                }
                if( error.id == "amount"){
                    $("#amount").addClass("is-invalid")
                    $("#amount-div").addClass("is-invalid")
                    $("#invalid-amount").html(error.message)
                }
                if( error.id == "description"){
                    $("#des").addClass("is-invalid")
                    $("#invalid-des").html(error.message)
                }
                if( error.id == "category"){
                    $("#category").addClass("is-invalid")
                    $("#invalid-cat").html(error.message)
                }
                if( error.id == "subCategory"){
                    $("#subCategory").addClass("is-invalid")
                    $("#invalid-sub").html(error.message)
                }
                if( error.id == "accountName"){
                    $("#accountName").addClass("is-invalid")
                    $("#invalid-account").html(error.message)
                }
            })
        } else {
            window.location.href = "/budget";
        }
    })
}
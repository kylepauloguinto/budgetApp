document.addEventListener("DOMContentLoaded", function () {
    
    let url = window.location.href
    let path = url.split("/")[3]

    // 
    $( "#category" ).change(function() {
        let parentValue = this.value;

        if( parentValue != ""){
            $("#subCategory").val('').trigger('change');
            document.getElementById("subCategory").removeAttribute("hidden");

            let option = document.getElementById("subCategory").options.length;
            let subCategory =  document.getElementById("subCategory");
            let hiddentCount = 0;

            for(let i = 0 ; i < option ; i++){
                let value = subCategory.options[i].value ;
                value = value.split("-")
                if(parentValue != value[0]){
                    hiddentCount++;
                    subCategory.options[i].setAttribute("hidden", "hidden");
                }else{
                    subCategory.options[i].removeAttribute("hidden");
                }
            }
            if(option == hiddentCount){
                document.getElementById("subCategory").setAttribute("hidden", "hidden");
            }
        }else{
            $("#subCategory").val('').trigger('change');
            document.getElementById("subCategory").setAttribute("hidden", "hidden");
        }
    });

    $( "#category-debit" ).change(function() {
        let parentValue = this.value;

        if( parentValue != ""){
            $("#subCategory-debit").val('').trigger('change');
            document.getElementById("subCategory-debit").removeAttribute("hidden");

            let option = document.getElementById("subCategory-debit").options.length;
            let subCategory =  document.getElementById("subCategory-debit");
            let hiddentCount = 0;

            for(let i = 0 ; i < option ; i++){
                let value = subCategory.options[i].value ;
                value = value.split("-")
                if(parentValue != value[0]){
                    hiddentCount++;
                    subCategory.options[i].setAttribute("hidden", "hidden");
                }else{
                    subCategory.options[i].removeAttribute("hidden");
                }
            }
            if(option == hiddentCount){
                document.getElementById("subCategory-debit").setAttribute("hidden", "hidden");
            }
        }else{
            $("#subCategory-debit").val('').trigger('change');
            document.getElementById("subCategory-debit").setAttribute("hidden", "hidden");
        }
    });


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
    });

    if( path == 'addTransaction' ){
        $( "#pills-transfer-tab" ).click(function() {
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
    }else if( path == 'editTransaction' ){
        //credit subCategory function
        let category =  document.getElementById("category").value ;
        document.getElementById("subCategory").removeAttribute("hidden");

        let option = document.getElementById("subCategory").options.length;
        let subCategory =  document.getElementById("subCategory");
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

        //debit subCategory function
        category =  document.getElementById("category-debit").value ;
        document.getElementById("subCategory-debit").removeAttribute("hidden");

        option = document.getElementById("subCategory-debit").options.length;
        subCategory =  document.getElementById("subCategory-debit");
        hiddentCount = 0;

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
        
        //transfer function accountFrom and accountTo 
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
        let id = url.split("/")[4]
        fetch(`transaction/${id}`)
        .then(response => response.json())
        .then(transaction =>{
            let mainDiv = document.getElementById("mainContainer");

            console.log(transaction)
            transaction.forEach(data => {

                //transaction information
                const main = document.createElement('div');
                main.setAttribute('class','dropright');
                const a = document.createElement('a');
                a.setAttribute('class','list-group-item list-group-item-action inbx-clck fs-2');
                a.setAttribute('href',"#");
                a.setAttribute('id','dropdownMenuLink');
                a.setAttribute('role','button');
                a.setAttribute('data-toggle','dropdown');
                a.setAttribute('aria-haspopup','true');
                a.setAttribute('aria-expanded','false');

                //transaction description
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

                //transfer information
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

                //notification badge
                if( data.readTransaction == false){
                    const span = document.createElement('span');
                    span.setAttribute('class','position-absolute top-0 start-100 translate-middle p-2 badge rounded-pill bg-danger')
                    span.innerHTML = ' ';
                    a.append(span);
                }

                //dropdown menu
                const divMenu = document.createElement('div');
                divMenu.setAttribute('class','dropdown-menu');
                divMenu.setAttribute('aria-labelledby','dropdownMenuLink');
                const aEdit = document.createElement('a');
                const aDuplicate = document.createElement('a');
                const aNote = document.createElement('a');
                const aDelete = document.createElement('a');
                aEdit.setAttribute('class','dropdown-item');
                aDuplicate.setAttribute('class','dropdown-item');
                aNote.setAttribute('class','dropdown-item');
                aDelete.setAttribute('class','dropdown-item');
                aEdit.setAttribute('href',`editTransaction/${data.id}`);
                const iEdit = document.createElement('i');
                const iDuplicate = document.createElement('i');
                const iNote = document.createElement('i');
                const iDelete = document.createElement('i');
                iEdit.setAttribute('class','bi bi-pencil');
                iDuplicate.setAttribute('class','bi bi-layers-fill');
                iNote.setAttribute('class','bi bi-pencil-square');
                iDelete.setAttribute('class','bi bi-trash3');
                aEdit.append(iEdit);
                aEdit.append('Edit');
                aDuplicate.append(iDuplicate);
                aDuplicate.append('Duplicate');
                aNote.append(iNote);
                aNote.append('Note');
                aDelete.append(iDelete);
                aDelete.append('Delete');
                const divDivider = document.createElement('div');
                divDivider.setAttribute('class','dropdown-divider');
                divMenu.append(aEdit);
                divMenu.append(aDuplicate);
                divMenu.append(aNote);
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
});
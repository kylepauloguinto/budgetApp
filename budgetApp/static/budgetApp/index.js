document.addEventListener("DOMContentLoaded", function () {
    
    let url = window.location.href
    let path = url.split("/")[3]

    $( "#classification" ).change(function() {
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

    $( "#classification-debit" ).change(function() {
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
        let category =  document.getElementById("classification").value ;
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
        category =  document.getElementById("classification-debit").value ;
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
        fetch(`unread/${id}`)
        .then(response => response.json())
        .then(message =>{
            console.log(message)
        })
    }
});
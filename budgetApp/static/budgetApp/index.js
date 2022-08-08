document.addEventListener("DOMContentLoaded", function () {
    
    
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

        if( accountNameFrom != ""){
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
        }else{
            $("#accountNameTo").val('').trigger('change');
            let option = document.getElementById("accountNameTo").options.length;
            let accountNameTo =  document.getElementById("accountNameTo");

            for(let i = 0 ; i < option ; i++){
                    accountNameTo.options[i].removeAttribute("hidden");
            }
        }
    });
});
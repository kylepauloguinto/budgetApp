document.addEventListener("DOMContentLoaded", function () {
    
    
    $( "#classification" ).change(function() {

        let parentValue = this.value;

        if( parentValue != ""){
            document.getElementById("category").removeAttribute("hidden");

            let option = document.getElementById("category").options.length;
            let subCategory =  document.getElementById("category");
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
                document.getElementById("category").setAttribute("hidden", "hidden");
            }
        }else{
            document.getElementById("category").setAttribute("hidden", "hidden");
        }
      });
});
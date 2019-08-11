function collapse_menu(collapse_id, icon_id) {
   
    
    var collapsable = document.getElementById(collapse_id);
    if (collapsable.style.display === "none") {
        collapsable.style.display = "block";
        document.getElementById(icon_id).innerHTML = '-';

    } else {
        collapsable.style.display = "none";
        document.getElementById(icon_id).innerHTML = '+';
       
    }
}
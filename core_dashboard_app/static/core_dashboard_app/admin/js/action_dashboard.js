
/**
* JS script that allows to do the action on the user dashboard
*/
action_dashboard = function(selectValue) {
    // Delete document
    if (selectValue == 1) {
        openDeleteDocument();
    }
    // Change owner document
    else if (selectValue == 2) {
        changeOwnerDocument();
    }
}
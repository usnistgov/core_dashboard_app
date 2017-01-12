
/**
* JS script that allows to do the action on the user dashboard
*/
action_dashboard = function(selectValue) {
    // Delete record
    if (selectValue == 1) {
        openDeleteRecord();
    }
    // Change owner record
    else if (selectValue == 2) {
        changeOwnerRecord();
    }
}
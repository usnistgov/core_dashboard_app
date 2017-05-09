/**
 * Get list of document selected
 * @returns {Array}
 */
getSelectedDocument = function () {
    var selected = [];
    if (isUserStaff == "True"){
        $('#actionCheckbox input:checked').each(function() {
            selected.push($(this).attr('id'));
        });
    } else {
        selected.push($('.'+functional_object+'-id').val());
    }
    return selected;
}
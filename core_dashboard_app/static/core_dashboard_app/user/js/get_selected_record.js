/**
 * Get list of record selected
 * @returns {Array}
 */
getSelectedRecord = function () {
    var selected = [];
    if (isUserStaff == "True"){
        $('#actionCheckbox input:checked').each(function() {
            selected.push($(this).attr('id'));
        });
    } else {
        selected.push($('.record-id').val());
    }
    return selected;
}
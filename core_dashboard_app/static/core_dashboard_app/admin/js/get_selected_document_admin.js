/**
 * Get list of document selected
 * @returns {Array}
 */
getSelectedDocument = function () {
    var selected = [];
    var val = $('.'+functional_object+'-id').val();
    if (val != "" ) {
        selected.push(val);
    } else {
        $('#actionCheckbox input:checked').each(function() {
            selected.push($(this).attr('id'));
        });
    }

    return selected;
};
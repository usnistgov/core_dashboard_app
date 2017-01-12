/**
 * Select all checkboxes
 */
function selectAll(source, id) {
    var isChecked = source.checked;
    $('input[name='+id+']').each(function() {
            $(this).prop("checked", isChecked);
        }
    );
}

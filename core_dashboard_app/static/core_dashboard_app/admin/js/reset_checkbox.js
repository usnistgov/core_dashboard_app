/**
 * Reset other checkbox
 */
function resetOtherCheckBox() {
    $('input[name=other]').each(function() {
           $(this).prop("checked", false);
        }
    );
    $('#select_all_other').prop('checked', false);

}

/**
 * Reset admin checkbox
 */
function resetAdminCheckBox() {
    $('input[name=admin]').each(function() {
           $(this).prop("checked", false);
        }
    );
    $('#select_all_admin').prop('checked', false);
}

/**
 * Reset all checkboxes
 */
function resetCheckbox() {
    resetAdminCheckBox();
    resetOtherCheckBox();
    countChecked();
    $( "input[type=checkbox]" ).on( "change", countChecked );
    $('.paginate_button ').on('click', resetCheckbox);
}

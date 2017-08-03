/**
 * Init the dropdown menu
 */
function initMenu() {
    resetCheckbox();
    $('.paginate_button ').on('click', resetCheckbox);
    countChecked();
    $( "input[type=checkbox]" ).on( "change", countChecked );
}
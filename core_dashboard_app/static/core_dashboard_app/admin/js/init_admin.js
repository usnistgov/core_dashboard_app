/**
* Init the tables. Count the number of checked boxes to control visibility of action dropdown
*/
function initAdminContext() {
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $.fn.dataTable
            .tables( { visible: true, api: true } )
            .columns.adjust();
    });
}

/**
 * Init on the admin side
 */
function init() {
    initAdmin();
    initAdminContext();
    if (menu) {
        initAdminMenu();
    }
}

/**
 * Init the dropdown menu
 */
function initAdminMenu() {
    resetCheckbox();
    $('.paginate_button ').on('click', resetCheckbox);
    countChecked();
    $( "input[type=checkbox]" ).on( "change", countChecked );
}
/**
* Init the tables. Count the number of checked boxes to control visibility of action dropdown
*/
function initAdminContext() {

    countChecked();
    $( "input[type=checkbox]" ).on( "change", countChecked );

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $.fn.dataTable
            .tables( { visible: true, api: true } )
            .columns.adjust();
    })

    $('.paginate_button ').on('click', resetCheckbox);
}

/**
 * Init on the admin side
 */
function init() {
    initAdmin();
    resetCheckbox();
    initAdminContext();
}
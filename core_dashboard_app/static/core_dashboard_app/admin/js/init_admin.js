/**
* Init the tables. Count the number of checked boxes to control visibility of action dropdown
*/
function initAdminContext() {
    initAdmin();

    countChecked();
    $( "input[type=checkbox]" ).on( "change", countChecked );

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $.fn.dataTable
            .tables( { visible: true, api: true } )
            .columns.adjust();
    })
}
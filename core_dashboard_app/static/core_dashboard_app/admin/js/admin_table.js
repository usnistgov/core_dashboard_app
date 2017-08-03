/**
 * Define the table for the forms
 */
function initAdmin() {
    if ( ! $.fn.dataTable.isDataTable( '#table-' + object + '-admin' ) ) {
        $('#table-' + object + '-admin').DataTable({
            "scrollY": "226px",
            "iDisplayLength": 5,
            "scrollCollapse": true,
            "lengthMenu": [5, 10, 15, 20],
            "columnDefs": [
                {"className": "dt-center", "targets": 0}
            ],
            order: [[2, 'asc']],
            "columns": getColumns()
        });
    }

    if ( ! $.fn.dataTable.isDataTable( '#table-' + object + '-other' ) ) {
        $('#table-' + object + '-other').DataTable({
            "scrollY": "226px",
            "iDisplayLength": 5,
            "scrollCollapse": true,
            "lengthMenu": [5, 10, 15, 20],
            "columnDefs": [
                {"className": "dt-center", "targets": 0}
            ],
            order: [[2, 'asc']],
            "columns": getColumns()
        });
    }
}

/**
 * Return the definition of the columns
 */
function getColumns() {

    if (numberColumns == "5") {
        return [ { "orderable": false }, null, null, null, { "orderable": false } ];
    }
    else if (numberColumns == "6") {
        return [ { "orderable": false }, null, null, null, null, { "orderable": false } ];
    }
    return [ null, null, null, { "orderable": false } ]

}
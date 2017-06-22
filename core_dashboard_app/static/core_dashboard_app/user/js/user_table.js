function initUser() {
    if ( ! $.fn.dataTable.isDataTable( '#table-' + object + '-user' )) {
        $('#table-' + object + '-user').DataTable({
            "scrollY": "226px",
            "iDisplayLength": 5,
            "scrollCollapse": true,
            "lengthMenu": [5, 10, 15, 20],
            "columnDefs": [
                {"className": "dt-center", "targets": 0}
            ],
            order: [[1, 'asc']],
            "columns": [null, null, {"orderable": false}]
        });
    }
}
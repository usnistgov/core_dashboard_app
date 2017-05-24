/**
 * Define the table for the types and templates
 */
function initAdmin() {
    $('#table-'+object+'-admin').DataTable({
        "scrollY": "226px",
        "iDisplayLength": 5,
        "scrollCollapse": true,
        "lengthMenu": [ 5, 10, 15, 20 ],
        "columnDefs": [
                {"className": "dt-center", "targets": 0}
              ],
        order: [[2, 'asc']],
        "columns": [ null, null, null, { "orderable": false } ]
    });

    $('#table-'+object+'-other').DataTable({
        "scrollY": "226px",
        "iDisplayLength": 5,
        "scrollCollapse": true,
        "lengthMenu": [ 5, 10, 15, 20 ],
        "columnDefs": [
                {"className": "dt-center", "targets": 0}
              ],
        order: [[2, 'asc']],
        "columns": [ null, null, null, { "orderable": false } ]
    });
}

function initUser() {
    $('#table-'+object+'-user').DataTable({
        "scrollY": "226px",
        "iDisplayLength": 5,
        "scrollCollapse": true,
        "lengthMenu": [ 5, 10, 15, 20 ],
        "columnDefs": [
                {"className": "dt-center", "targets": 0}
              ],
        order: [[1, 'asc']],
        "columns": [ null, null, { "orderable": false } ]
    });
}
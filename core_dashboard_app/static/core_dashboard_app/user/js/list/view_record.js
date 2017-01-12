openViewRecord = function() {
    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");

    window.location = viewRecordUrl + '?id=' + objectID;
}

$(".view-record-btn").on('click', openViewRecord);

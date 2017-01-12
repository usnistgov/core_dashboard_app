
/**
 * Open the modal before deleting the record
 */
openDeleteRecord = function () {
    if (isUserStaff == "False") {
        var $recordRow = $(this).parent().parent();
        $('.record-id').val($recordRow.attr("objectid"));
    }
    $("#delete-result-modal").modal("show");
}

/**
 * AJAX call, delete a curated document
 * @param result_id
 */
delete_record = function(){
	$.ajax({
        url : dashboardDeleteRecordUrl,
        type : "POST",
        dataType: "json",
        data : {
        	record_id: getSelectedRecord()
        },
		success: function(data){
		        location.reload(true);
	    }
    });
}


$('.delete-result-btn').on('click', openDeleteRecord);
$('#delete-result-yes').on('click', delete_record);

/**
 * Get the URL to go to the edit page
 */
openEditRecord = function() {
    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");

    $.ajax({
        url : editRecordUrl,
        type : "POST",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            window.location = data.url;
        }
    });
};

$(".edit-record-btn").on('click', openEditRecord);
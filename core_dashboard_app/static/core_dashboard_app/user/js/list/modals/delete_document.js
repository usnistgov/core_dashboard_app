
/**
 * Open the modal before deleting the document
 */
openDeleteDocument = function () {
    var $recordRow = $(this).parent().parent();
    $('.'+functional_object+'-id').val($recordRow.attr("objectid"));
    $("#delete-result-modal").modal("show");
};

/**
 * AJAX call, delete a curated document
 * @param result_id
 */
delete_document = function(){
	$.ajax({
        url : dashboardDeleteDocumentUrl,
        type : "POST",
        dataType: "json",
        data : {
        	document_id: getSelectedDocument(),
            functional_object: functional_object
        },
		success: function(data){
		        location.reload(true);
	    }
    });
};


$('.delete-document-btn').on('click', openDeleteDocument);
$('#delete-document-yes').on('click', delete_document);

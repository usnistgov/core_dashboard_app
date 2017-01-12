/**
 * Change record owner
 */
changeOwnerRecord = function() {
    if (isUserStaff == "False") {
        var $recordRow = $(this).parent().parent();
        $('.record-id').val($recordRow.attr("objectid"));
    }
    $("#banner_errors").hide();
    $("#change-owner-modal").modal("show");
};

/**
 * Validate fields of the change owner modal
 */
validateChangeOwner = function(){
    var errors = "";

    $("#banner_errors").hide();
    // check if a user has been selected
    if ($( "#id_users" ).val().trim() == ""){
        errors = "Please provide a user."
    }

    if (errors != ""){
        $("#form_start_errors").html(errors);
        $("#banner_errors").show(500);
        return (false);
    }else{
        return (true);
    }
};


/**
 * AJAX call, change record owner
 */
change_owner_record = function(){
    var userId = $( "#id_users" ).val().trim();
    $.ajax({
        url : dashboardChangeOwnerUrl,
        type : "POST",
        dataType: "json",
        data : {
            recordID: getSelectedRecord(),
            userID: userId
        },
		success: function(data){
			location.reload();
	    },
        error:function(data){
            $("#form_start_errors").html(data.responseText);
            $("#banner_errors").show(500)
        }
    });
};

/**
 * Validate and change the owner
 */
validate_and_change_owner = function () {
    if (validateChangeOwner()) {
        var formData = new FormData($( "#form_start" )[0]);
        change_owner_record();
    }
};


$('.change-owner-btn').on('click', changeOwnerRecord);
$('#change-owner-yes').on('click', validate_and_change_owner);
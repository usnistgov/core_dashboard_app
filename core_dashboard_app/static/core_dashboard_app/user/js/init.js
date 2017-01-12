$(document).ready(function(){
    $("[data-hide]").on("click", function(){
        $(this).closest("." + $(this).attr("data-hide")).hide(200);
    });

    if (isUserStaff == "True") {
        initRecordAdmin();
        initAdmin();
    } else {
        initRecordUser();
    }
    resetCheckbox();

    $('.paginate_button ').on('click', resetCheckbox);
});
$(document).ready(function(){
    $("[data-hide]").on("click", function(){
        $(this).closest("." + $(this).attr("data-hide")).hide(200);
    });

    if (isUserStaff == "True") {
        initAdminContext();
    } else {
        initUser();
    }
    resetCheckbox();

    $('.paginate_button ').on('click', resetCheckbox);
});
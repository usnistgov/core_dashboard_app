/**
 * my_dashboard_tabs javascript file
 */

/**
 * Update URL
 */
redirect_to = function(tab, page) {
    var url = urlResources;
    // add the tab we are on
    url += "?tab=" + tab;
    // add the page number
    if (page !== '' && page !== '1') {
        url += '&page=' + page;
    }
    // redirect
    window.location.href = url;
};

/**
 * When a tab is clicked
 */
var onTabClicked = function(event) {
    $(document.body).css({'cursor' : 'wait'});
    redirect_to(event.currentTarget.dataset.tabValue, 1);
}

$(document).ready(function() {
    $("a[id^='tab_']").on('click', onTabClicked);
});
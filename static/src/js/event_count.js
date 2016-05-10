$(function() {
    var table = $('.event-count-table-container'),
        region = table.data().region || "overall",
        fy = table.data().financialYear || "0",
        ajaxUrl = table.data().url + region + '/' + fy + '/';

    table.load(ajaxUrl, function(response, status, xhr) {
        this.html(response);
        this.find('table.event-count-table').DataTable({
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]]
        });
    });
});
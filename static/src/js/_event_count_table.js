// NOTE: This is basically an initialization function. Consider putting this with other intialization functions in
// src/main.js
document.addEventListener('DOMContentLoaded', function() {
    var tableContainers = document.querySelectorAll('.event-count-table-container');
    if (tableContainers.length) {
        for (var i = 0; i < tableContainers.length; i++) {
            initializeEventCountTable(tableContainers[i]);
        }
    }
});


// NOTE: This function is almost identical to the one in src/_event_count_table.js. Strongly consider extracting
// this to a shareable function that can be called from both places.
function initializeEventCountTable(tableContainer) {
    var region = tableContainer.dataset.region || "overall",
        fy = tableContainer.dataset.financialYear || "0",
        ajaxUrl = tableContainer.dataset.url + region + '/' + fy + '/';

    $(tableContainer).load(ajaxUrl, function(response, status, xhr) {
        this.html(response);
        this.find('table.event-count-table').DataTable({
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]]
        });
    });
}
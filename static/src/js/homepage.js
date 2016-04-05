var glmap = require('./modules/glmap');


document.addEventListener('DOMContentLoaded', function () {

    // Initialize GL map on the home screen
    if (document.querySelector('#mapcontainer')) {
        glmap.drawMap();
    }

    // Listen for download trigger
    $(document).on("click", ".btn-export-map", function () {
        glmap.submitDownloadForm("pdf");
    });
});
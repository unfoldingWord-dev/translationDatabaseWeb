require("../less/site.less");

window.jQuery = window.$ = require("jquery");

require("bootstrap");
require("bootstrap-datepicker");
require("imports?define=>false!bootstrap-daterangepicker");
require("eldarion-ajax");
require("select2");
require("datatables");
require("datatables-bootstrap3-plugin");


// Custom init for select2 language search input
$.fn.languageSelector = function(options) {
    var settings = $.extend({}, options);
    return this.each(function () {
        var $input = $(this);
        $input.select2({
            placeholder: "Search for a language...",
            minimumInputLength: 2,
            ajax: {
                url: $input.data("source-url"),
                dataType: "json",
                quietMillis: 250,
                data: function (term, page) {
                    return {q: term};
                },
                results: function (data, page) {
                    return {results: data.results};
                },
                cache: true
            },
            initSelection: function (element, callback) {
                var data = {
                    "pk": element.data("lang-pk"),
                    "ln": element.data("lang-ln"),
                    "lc": element.data("lang-lc"),
                    "lr": element.data("lang-lr")
                };
                callback(data);
            },
            id: function (lang) { return lang.pk; },
            formatResult: function (lang) {
                return "<strong>" + lang.ln + "</strong> <code>" + lang.lc + "</code> [" + lang.lr + "]";
            },
            formatSelection: function (lang) {
                return "<strong>" + lang.ln + "</strong> <code>" + lang.lc + "</code> [" + lang.lr + "]";
            },
            escapeMarkup: function (m) {
                return m;
            }
        });
    });
};
// Set default init for DataTables
$.fn.customDataTable = function(options) {
    var defaults = {
        stateSave: true,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]]
    };
    return $(this).DataTable($.extend(defaults, options));
};

// Initialize components
(function ($) {

    // Initialize bootstrap components
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();
    $(".date-picker").daterangepicker({
      singleDatePicker: true
    });

    // Initialize select2 components
    $(".select2-multiple").select2();
    $(".language-selector").languageSelector();

    // Initialize DataTables (serverSide)
    $("table[data-source]").each(function () {
        var $el = $(this);
        $el.customDataTable({
            serverSide: true,
            ajax: $el.data("source"),
        });
    });

    // Initialize DataTables (clientSide)
    $('table.js-datatable').customDataTable();

    // Initialize event-count tables
    $('.event-count-table-container').each(function() {
        var mode = this.dataset.mode || "dashboard",
            option = this.dataset.option || "overall",
            fy = this.dataset.fiscalYear || "0",
            ajaxUrl = this.dataset.url + mode + '/' + option + '/' + fy + '/',
            loading = $(this).siblings('.loading');

        loading && loading.show();
        $(this).load(ajaxUrl, function(response, status, xhr) {
            this.html(response);
            this.find('table.event-count-table').customDataTable();
            loading && (loading.hide());
        });
    });

})(jQuery);


// Register event listeners
$(function () {
    // Display invite confirmation when it's sent
    $(document).on("eldarion-ajax:success", function (evt, $el) {
        if ($el.hasClass("navbar-form")) {
            var $el = $("<div>")
              .addClass("alert")
              .addClass("alert-info")
              .html("<strong>Invite was sent!</sent>");
            $("body").prepend($el);
            setTimeout(function(){ $el.remove(); }, 3000);
        }
    });

    // Swap expand/collapse icons for button that toggle bootstrap collapse
    $('body').on("click", "[data-toggle='collapse']", function() {
        $(this).find('i').toggleClass("fa-expand fa-compress");
    });
});

// Custom scripts for specific web pages
require("./homepage.js");
require("./language_list.js");
require("./tracking_forms.js");

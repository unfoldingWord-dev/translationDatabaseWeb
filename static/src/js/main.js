require("../less/site.less");

window.jQuery = window.$ = require("jquery");

// Requirements for td.tracking
require("./tracking_forms.js");

require("bootstrap");
require("bootstrap-datepicker");
require("imports?define=>false!bootstrap-daterangepicker");
require("eldarion-ajax");
require("select2");
require("datatables");
require("datatables-bootstrap3-plugin");

var glmap = require("./glmap");


(function ($) {
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();
    if (document.getElementById('mapcontainer') !== null) glmap.drawMap();
    $(document).on("click", ".btn-export-map", function() {glmap.submitDownloadForm("pdf");});
    $.fn.languageSelector = function (options) {
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
              escapeMarkup: function (m) { return m; }
            });
        });
    };
})(jQuery);

$(function () {
    $("table[data-source]").each(function () {
        var $el = $(this);
        $el.DataTable({
            serverSide: true,
            ajax: $el.data("source"),
            stateSave: true
        });
    });
    $(".select2-multiple").select2();
    $(".language-selector").languageSelector();
    $(".date-picker").daterangepicker({
      singleDatePicker: true
    });
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
    // Swapping expand and compress icons on element that toggles bootstrap collapse
    $('body').on("click", "[data-toggle='collapse']", function() {
        $(this).find('i').toggleClass("fa-expand fa-compress");
    });
});

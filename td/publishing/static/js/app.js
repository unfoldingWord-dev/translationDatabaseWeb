(function ($) {
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
                  return {q: term}
                },
                results: function (data, page) {
                  return {results: data.results}
                },
                cache: true
              },
              initSelection: function (element, callback) {
                data = {
                  "pk": element.data("lang-pk"),
                  "ln": element.data("lang-ln"),
                  "lc": element.data("lang-lc"),
                  "gl": element.data("lang-gl")
                }
                callback(data);
              },
              id: function (lang) { return lang.pk; },
              formatResult: function (lang) {
                gl = "";
                if (lang.gl) gl = "[gateway]";
                return "<strong>" + lang.ln + "</strong> <code>" + lang.lc + "</code> " + gl;
              },
              formatSelection: function (lang) {
                gl = "";
                if (lang.gl) gl = "[gateway]";
                return "<strong>" + lang.ln + "</strong> <code>" + lang.lc + "</code> " + gl;
              },
              escapeMarkup: function (m) { return m; }
            });
        });
    }
})(jQuery);

$(function () {
    $(".language-selector").languageSelector();
});


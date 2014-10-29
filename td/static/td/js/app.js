$(function () {
    $("table[data-source]").each(function () {
        var $el = $(this);
        $el.DataTable({
            serverSide: true,
            ajax: $el.data("source"),
            stateSave: true
        });
    });
});

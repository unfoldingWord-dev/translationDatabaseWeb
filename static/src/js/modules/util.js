/**
 * Created by leongv on 3/15/2016.
 */

var util = {
    /*
     * Returns the value of a specified parameter in the URL
     * @param name: The name of parameter in string
     * @param url: URL string (optional)
     * :return: Retrieved value, or empty string, or null
     */
    getParamByName: function(name, url) {
        var url = (url || window.location.href).toLowerCase(),
            name = name.replace(/[\[\]]/g, "\\$&").toLowerCase(),
            regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) { return null; }
        if (!results[2]) { return ''; }
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    },

    dtTriggerSearch: function(s, q) {
        if (!s || !q) { return; }
        s.value = q;
        // DataTables listens to 'search' event (https://datatables.net/reference/event/)
        // If event is cancelled, dispatchEvent will return false.
        return s.dispatchEvent(new Event('search'));
    }
};

module.exports = util;

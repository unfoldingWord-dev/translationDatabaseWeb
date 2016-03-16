/**
 * Created by leongv on 3/15/2016.
 */

var util = require('./modules/util');

document.addEventListener('DOMContentLoaded', function () {
    // Enter the search term passed through the URL into the search box
    // NOTE: DataTables will append "_wrapper" to the table's ID
    var searchBox = document.querySelector('#language-list-table_wrapper input[type="search"]'),
        q = util.getParamByName('q') || '';
    searchBox && q ? util.dtTriggerSearch(searchBox, q) : undefined;
});

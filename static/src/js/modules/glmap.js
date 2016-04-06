var $ = require("jquery");
var d3 = require("d3");
var Datamap = require("datamaps/dist/datamaps.world");

var m_width = $("#mapcontainer").width(),
              m_ratio = .42,
              m_height = m_width * m_ratio;

module.exports = {
    drawMap: function () {
        // @@@ pull this url from a data- attribute so we can use url reverser and not hardcode the url
        d3.json("/uw/country_map_data.json", function(error, map_data) {
            var map = new Datamap({
                element: document.getElementById('mapcontainer'),
                responsive: true,
                width: m_width,
                height: m_height,
                fills: map_data["fills"],
                data: map_data["country_data"],
                geographyConfig: {
                    hideAntarctica: true,
                    borderColor: "#202020",
                    highlightOnHover: true,
                    highlightBorderWidth: 2,
                    highlightFillColor: 'rgba(128,128,128,0.5)',
                    popupTemplate: function(geography, data) {
                        if (data) {
                            geography.properties.url = data.url;
                            return '<div class="hoverinfo"><div class="flag flag-' +
                                    data.country_code.toLowerCase() + '"> </div><strong>' +
                                    geography.properties.name + '</strong><br/>' +
                                    data.gateway_languages.join('<br/>') +
                                    '</div>';
                        }
                        else
                            return '<div class="hoverinfo"><strong>' + geography.properties.name + '</strong></div>';
                    }
                },
                done: function(datamap) {
                    datamap.svg.selectAll('.datamaps-subunit').on('click', function(geography) {
                        var $this = d3.select(this);
                        var previousAttributes = JSON.parse( $this.attr('data-previousAttributes') );
                            for ( var attr in previousAttributes ) {
                                $this.style(attr, previousAttributes[attr]);
                            }
                        window.location.href = geography.properties.url;
                    });
                    this.element.style.paddingBottom = "38%";
                }
            });

            d3.select(window).on('resize', function() {
                map.resize();
            })
        })
    },

    submitDownloadForm: function(output_format) {
        // Get the d3js SVG element
        var tmp = document.getElementById("mapcontainer");
        var svg = tmp.getElementsByTagName("svg")[0];
        // Extract the data as SVG text string
        var svg_xml = (new XMLSerializer).serializeToString(svg);

        // Submit the <FORM> to the server.
        // The result will be a file to download.
        var form = document.getElementById("svgform");
        form['output_format'].value = output_format;
        form['data'].value = svg_xml ;
        form.submit();
    }
};

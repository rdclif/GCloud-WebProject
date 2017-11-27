var map;
$(document).ready(function() {
    //zip code search form
    $('#zip-search').submit(function(event) {
        event.preventDefault();
        zip = $('#zip').val();
        dist = $('#dist').val();
        var zip_table = $('#zip-table');
        if (dist === null) {
            zip_table.empty();
            zip_table.append("<tr><td>Error: Please input a radius.</td></tr>");
        } else {
            $.ajax({
                dataType: "json",
                method: "post",
                url: "/zipRequest/" + zip + "/" + dist,
                success: function (data) {
                    if (data[1].length === 0) {
                        zip_table.empty();
                        zip_table.append("<tr><td>No ZIP Codes within a "+dist+" mile radius of "+zip+".</td></tr>");
                    } else {
                        var count = 0;
                        zip_table.empty();
                        zip_table.append("<tr><td>#</td><td>Zip</td><td>City</td><td>State</td></tr>");
                        $.each(data[1], function () {
                            count += 1;
                            zip_table.append("<tr><td>" + count.toString() + "</td><td>" + this.zip + "</td><td>" + this.city + "</td><td>" + this.st + "</td></tr>");
                        });
                        updateMap(data[0], data[1]);
                    }
                },
                error: function () {
                    zip_table.empty();
                    zip_table.append("<tr><td>An error occurred. Check your input and try again.</td></tr>");
                }
            });
        }
        return false;
    });
});

function loadScript(src,callback){
    var script = document.createElement("script");
    script.type = "text/javascript";
    if(callback)script.onload=callback;
    document.getElementsByTagName("head")[0].appendChild(script);
    script.src = src;
}
loadScript('https://maps.googleapis.com/maps/api/js?key=AIzaSyABV_iEVDj2ccF50CJMD8kO3o5mbLr2SX4&callback=initMap',
    function(){log('google-loader has been loaded, but not the maps-API ');});

function initMap() {

    log('maps-API has been loaded, ready to use');
    var mapOptions = {
          zoom: 8,
          center: new google.maps.LatLng(45.527, -122.685),
          mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map'),
            mapOptions);
  }

function log(str){
  console.log(str);
}

function updateMap(center, points) {
    var lal = {lat: center['lat'], lng:center['lon']};
    var mapOptions = {
        center: lal,
        zoom: 10
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    for (var i = 0; i < points.length; i++) {
        var count = i+1;
        var coord = {lat: points[i]['lat'], lng:points[i]['lon']};
        var marker = new google.maps.Marker({
            position: coord,
            map: map,
            label: count.toString()
        });
    }
}
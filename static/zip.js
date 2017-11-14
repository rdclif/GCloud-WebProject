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
                    if (data.length === 0) {
                        zip_table.empty();
                        zip_table.append("<tr><td>No ZIP Codes within a "+dist+" mile radius of "+zip+".</td></tr>");
                    } else {
                        zip_table.empty();
                        zip_table.append("<tr><td>Zip</td><td>City</td><td>State</td></tr>");
                        $.each(data, function () {
                            zip_table.append("<tr><td>" + this.zip + "</td><td>" + this.city + "</td><td>" + this.st + "</td></tr>");
                        });
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
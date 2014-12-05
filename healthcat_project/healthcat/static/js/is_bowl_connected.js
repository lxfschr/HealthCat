var count = 0;

function is_bowl_connected() {
    console.log("in is_bowl_connected()");
    var serial_number = $("#serial_number").html();
    console.log("in serial_number: " + serial_number);
    
    var MAX_COUNT = 12;
    var WAIT_TIME = 5;
    $.ajax({
        // the URL for the request
        url: "/healthcat/is-bowl-connected?serial_number="+serial_number,

        // whether this is a POST or GET request
        type: "GET",
     
        // the type of data we expect back
        dataType : "json",
     
        // code to run if the request succeeds;
        // the response is passed to the function
        success: function( response ) {
            if(response['result'] == "SUCCESS") {
                document.location.href="/healthcat/profile";
            }
            else {
                console.log("count: " + count);
                if(count >= 12) {
                    document.location.href="/healthcat/failed-to-connect";
                }
                else {
                    count++;
                    window.setTimeout( is_bowl_connected, 5000 );
                }
            }
            console.log( "Success! " + response['result'] );
        },
     
        // code to run if the request fails; the raw request and
        // status codes are passed to the function
        error: function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        },
    });
    
    return false;
}

$(document).ready(function() {
    is_bowl_connected();
});
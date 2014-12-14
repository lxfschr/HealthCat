function update_notifications() {
    console.log("in update_notifications()");
    var notifications_list = $("#notifications_list");
    var last_notification_date = notifications_list.children(':first').attr('notification_date');

    console.log("last_notification_date: " + last_notification_date);

    $.ajax({
        // the URL for the request
        url: "/healthcat/notifications?date="+last_notification_date,
     
        // whether this is a POST or GET request
        type: "GET",
     
        // the type of data we expect back
        dataType : "html",
     
        // code to run if the request succeeds;
        // the response is passed to the function
        success: function( response ) {
            //append html
            notifications_list.prepend(response);
        },
     
        // code to run if the request fails; the raw request and
        // status codes are passed to the function
        error: function( xhr, status, errorThrown ) {
            //alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        },
     
        // code to run regardless of success or failure
        /*complete: function( xhr, status ) {
            alert( "The request is complete!" );
        }*/
    });
    return false;
}

// causes the update_stream function to run every 5 seconds
window.setInterval(update_notifications, 5000);
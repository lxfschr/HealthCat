$(document).ready(function(){
    replace_html("total_food_consumption_btn", "statistics_div", "total-consumption");
});

$('.stats-list').on('click', 'li', function() {
    $('.stats-list li.active').removeClass('active');
    $(this).addClass('active');
});

function replace_html(clicked_id, to_replace_id, url) {
	
	//jquery ajax
	// Using the core $.ajax() method
	$.ajax({
	    // the URL for the request
	    url: url,
	 
	    // whether this is a POST or GET request
	    type: "GET",
	 
	    // the type of data we expect back
	    dataType : "html",
	 
	    // code to run if the request succeeds;
	    // the response is passed to the function
	    success: function( response ) {
	    	console.log(response)
	    	$("#" + to_replace_id).html(response)
	    	console.log("success")
	    },
	 
	    // code to run if the request fails; the raw request and
	    // status codes are passed to the function
	    error: function( xhr, status, errorThrown ) {
	        alert( "Sorry, there was a problem!" );
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
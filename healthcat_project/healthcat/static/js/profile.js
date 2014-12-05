function delete_item(event, form_id, remove_id, url) {
	event.preventDefault();
	//select form element
	form = $("#"+form_id);
	//serialize it
	form = form.serialize();
	//jquery ajax
	// Using the core $.ajax() method
	$.ajax({
	    // the URL for the request
	    url: url,
	 
	    // the data to send (will be converted to a query string)
	    data: form,
	 
	    // whether this is a POST or GET request
	    type: "POST",
	 
	    // the type of data we expect back
	    dataType : "json",
	 
	    // code to run if the request succeeds;
	    // the response is passed to the function
	    success: function( response ) {
	    	$("#" + remove_id).remove()
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

function add_pet_form(event, form_id, pet_info_id, url) {
	event.preventDefault();
	//select form element
	form = $("#"+form_id);
	console.log("form: " + form);
	//serialize it
	form = form.serialize();
	console.log("event: ", event);
	var input_form = event.target;
	//jquery ajax
	// Using the core $.ajax() method
	$.ajax({
	    // the URL for the request
	    url: url,
	 
	    // the data to send (will be converted to a query string)
	    data: form,
	 
	    // whether this is a POST or GET request
	    type: "GET",
	 
	    // the type of data we expect back
	    dataType : "html",
	 
	    // code to run if the request succeeds;
	    // the response is passed to the function
	    success: function( response ) {
	    	console.log(response)
	    	$("#" + pet_info_id).replaceWith(response)
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

function add_bowl_form(event, id, url) {
	event.preventDefault();
	//select form element
	form = $("#"+id);
	console.log("form: " + form);
	//serialize it
	form = form.serialize();
	console.log("event: ", event);
	var input_form = event.target;
	//jquery ajax
	// Using the core $.ajax() method
	$.ajax({
	    // the URL for the request
	    url: url,
	 
	    // the data to send (will be converted to a query string)
	    data: form,
	 
	    // whether this is a POST or GET request
	    type: "GET",
	 
	    // the type of data we expect back
	    dataType : "html",
	 
	    // code to run if the request succeeds;
	    // the response is passed to the function
	    success: function( response ) {
	    	console.log(response)
	    	$("#" + id).replaceWith(response)
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

$(document).ready(function() {
	console.log("ready");
    $('#myModal').modal()
});
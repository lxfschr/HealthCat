

function add_edit_pet_form(pet_id, url) {
	id = pet_id + "_pet_info"
	console.log(url + "?pet_id=" + pet_id)
	$( "#" + id ).load( url + "?pet_id=" + pet_id);
}

function add_add_pet_form(bowl_id, url) {
	id = bowl_id + "_add_pet_text"
	$( "#" + id ).load( url );
}

function add_add_feeding_interval_form(pet_id, url) {
	id = pet_id + "_feeding_intervals"
	$( "#" + id ).load( url );
}

function add_edit_bowl_form(bowl_id, url) {
	id = bowl_id + "_bowl_name"
	$( "#" + id ).load( url );
}

function add_add_bowl_form(id, url) {
	$( "#add_bowl_text" ).load( url );
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
function add_add_bowl_form() {
	$( "#add_bowl_text" ).load( "/healthcat/add-bowl-form");
}

function add_comment(event, grumbl_id) {
	event.preventDefault();
	//select form element
	formid = grumbl_id + "_comment_form";
	form = $("#"+formid);
	console.log("form: " + form);
	//serialize it
	form = form.serialize();
	console.log("event: ", event);
	var input_form = event.target;
	
	//jquery ajax
	// Using the core $.ajax() method
	$.ajax({
	    // the URL for the request
	    url: "/grumblrApp/comment/"+grumbl_id,
	 
	    // the data to send (will be converted to a query string)
	    data: form,
	 
	    // whether this is a POST or GET request
	    type: "POST",
	 
	    // the type of data we expect back
	    dataType : "html",
	 
	    // code to run if the request succeeds;
	    // the response is passed to the function
	    success: function( response ) {
	    	//select grumbl_id comments
	    	comments = $("#"+grumbl_id+"_comments");
	    	//append html
	    	comments.append(response);
	    	console.log(input_form);
	    	$(input_form).find("input[type=text], textarea").val("");
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
$(document).ready(function(){
	//Get pet data
		function getPetData (email, callback){
			var baseURL = 'http://0.0.0.0:8080/api/pets';
			var owner_email = email;
			var settings = {
				url: baseURL, 
				data: {
					owner_email: owner_email
				}, 
				dataType: 'json',
				type: 'GET', 
				success: callback
			};
			$.ajax(settings);
		}	


	/*function generateResultsHTML(data){

	}*/

	function displayResults(data){
		console.log(data);
		/*generateResultsHTML(data);*/
	}

	$('.js-sign-in-form').submit(function(event){
		console.log("running");
		event.preventDefault();
		owner_email = $('.js-email').val();
		getPetData(owner_email, displayResults);
	});
});

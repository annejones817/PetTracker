$(document).ready(function(){
	//Get pet data
		function addPetPost(petName, petBirthDate) {
			var baseURL = '/api/add-pet';
			var obj = {
				"pet-name": petName, 
				"pet-birthdate": petBirthDate
			};
			console.log(obj);
			$.ajax({
				url: baseURL, 
				data: JSON.stringify(obj), 
				dataType: 'json',
				type: 'POST',
				contentType: 'application/json',
				success: function(data){
					console.log(data);
					if (data) {
						console.log(data);
						window.location.href="/dashboard";
					} else {
						console.log("fail");
					}
				}
			});
		}	

	//Initialize datepicker for birthdate	
	$('#datepicker').datepicker(
		{
		   dateFormat: "yy-mm-dd",
		   timeFormat:  "hh:mm:ss"
		}
	);	

	//Listen for add pet submit
	$('.js-add-pet-form').submit(function(event){
		console.log('clicked');
		event.preventDefault();
		//Check form 
		var petName = $('#pet-name').val();
		//Handle undefined
		var petBirthDate = $('#datepicker').val();
		addPetPost(petName, petBirthDate);
	})
	console.log("test");
});

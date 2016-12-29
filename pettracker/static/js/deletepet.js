$(document).ready(function(){
	//Send post request to delete pet
		function deletePetPost(petDeleteURL) {
			var baseURL = 'api/' + petDeleteURL;
			$.ajax({
				url: baseURL, 
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
	//Listen for delete pet
	$('.pets-container').on('click', '.delete-pet', function(event){
		console.log('clicked');
		var petDeleteURL = $(this).attr("id");
		deletePetPost(petDeleteURL);
		this.remove();
	});
});

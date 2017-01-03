$(document).ready(function(){
	//Functions
	function getProfileDetails(){
		var baseURL = 'api/profile-details';
		$.ajax({
			url: baseURL, 
			dataType: 'json', 
			type: 'GET', 
			contentType: 'application/json', 
			success: function(data){
				if (data) {
					populateProfile(data);
				} else {
					console.log("fail");
				}
			}
		});
	} 

	function populateProfile(data){
		$('.current-name-detail').append('<span>Name: ' + data.first_name + ' ' + data.last_name + '</span');
		$('#first-name').val(data.first_name); 
		$('#last-name').val(data.last_name);
		$('.current-email-detail').append('<span>Email: ' + data.email + '</span');
		$('#current-email').val(data.email);
	}

	//Populate details on page load
	getProfileDetails();
});
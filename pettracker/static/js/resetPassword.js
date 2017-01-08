$(document).ready(function(event){
	function resetPassword(data){
		//initialize variables
		var newPassword; 
		var confirmPassword; 

		//set variables
		newPassword = $('#new-password').val();
		confirmPassword = $('#confirm-password').val(); 

		//Check that new and confirm match  
		if (newPassword != confirmPassword) {
			$('.user-alerts').append('<span class="user-alert-detail">New password and confirm password do not match.</span>');
			return;
		}

		var obj = {
			"email": data.email, 
			"gid" : data.gid, 
			"new-password": newPassword
		}

		//Make API request to update password
		$.ajax({
			url: "/api/reset-password", 
			data: JSON.stringify(obj), 
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json',
			success: function(data){
				if (data.message == 'Successful reset') {
					window.location.href="/dashboard";
				} else {
					$('.user-alerts').append('<span class="user-alert-detail">Password reset failed. Please try again.</span>');
				}
			}
		});
	}

	//Listen for reset password click
	$('.reset-password-button').click(function(event){
		//get gid and email from url 
		var params = window.location.search.substring(1)
		var splitParams = params.split("&")
		var gid = splitParams[0].split("=")[1]
		var email = splitParams[1].split("=")[1]
		var data = {}; 
		data["gid"]= gid; 
		data["email"] = email;
		console.log(data);
		resetPassword(data);
	});
});
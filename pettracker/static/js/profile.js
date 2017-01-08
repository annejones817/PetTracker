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
		$('.profile-name').prepend('<div class="profile-detail current-name-detail"><span>Name: ' + data.first_name + ' ' + data.last_name + '</span></div>');
		$('#first-name').val(data.first_name); 
		$('#last-name').val(data.last_name);
		$('.profile-email').prepend('<div class="profile-detail current-email-detail"><span>Email: ' + data.email + '</span></div>');
		$('#current-email').val(data.email);
		$('.profile-password').prepend('<div class="profile-detail current-password">Password: &#42;&#42;&#42;&#42;&#42;&#42;&#42;</div>');
	}

	function saveProfile(data){
		//initialize variables 
		var firstName; 
		var lastName;
		var currentEmail; 
		var newEmail; 
		var confirmEmail; 
		var currentPassword; 
		var newPassword; 
		var confirmNewPassword;
		var obj = {};

		//set variables
		firstName = $('#first-name').val();
		obj["first-name"] = firstName;

		lastName = $('#last-name').val();
		obj["last-name"] = lastName;

		currentEmail = $('#current-email').val();
		obj["current-email"] = currentEmail; 

		newEmail = $('#new-email').val(); 
		obj["new-email"] = newEmail;

		confirmEmail = $('#confirm-email').val();
		//obj["confirm-email"] = confirmEmail; 

		currentPassword = $('#current-password').val();
		obj["current-password"] = currentPassword;

		newPassword = $('#new-password').val();
		obj["new-password"] = newPassword;

		confirmNewPassword = $('#confirm-password').val();
		//obj["confirm-password"] = confirmPassword;

		//Check new email and confirm email for match: 
		if (newEmail != confirmEmail) {
			$('.user-alerts').append('<span class="user-alert-detail">New email and confirm email do not match.</span>');
			return;
		}

		if (newPassword != confirmNewPassword) {
			$('.user-alerts').append('<span class="user-alert-detail">New password and confirm password do not match.</span>');
			return;
		}

		saveProfilePost(obj);

	}

	function saveProfilePost(obj){
		var baseURL = '/api/profile-update';
		$.ajax({
			url: baseURL, 
			data: JSON.stringify(obj), 
			dataType: 'json',
			type: 'POST', 
			contentType: 'application/json',
			success: function(data){
				console.log(data); 
				if (data) {
					$('.cancel-profile-button, .save-profile-button, .edit-profile-details').addClass('hidden');
					$('.edit-profile-button').removeClass("hidden");
					$('.user-alert-detail').remove();
					getProfileDetails();
				} else {
					console.log("no data");
				}
			}
		});
	}

	//Populate details on page load
	getProfileDetails();

	//////////Event Listeners
	//Click on edit profile button 
	$('.edit-profile-button').click(function(event){
		$(this).addClass("hidden");
		$('.profile-detail').remove(); 
		$('.edit-profile-details, .save-profile-button, .cancel-profile-button').removeClass("hidden");
	});

	//Click on cancel edit button 
	$('.cancel-profile-button').click(function(event){
		$('.cancel-profile-button, .save-profile-button, .edit-profile-details').addClass('hidden');
		$('.edit-profile-button').removeClass("hidden");
		$('.user-alert-detail').remove();
		getProfileDetails();
	});

	//Click on save details button 
	$('.save-profile-button').click(function(event){
		saveProfile();
	});
});
$(document).ready(function(){
	////Functions
	function joinPost(firstName, lastName, email, password) {
		console.log("function running")
		var baseURL = '/api/join'; 
		var obj = {
			"first_name": firstName,
			"last_name": lastName,
			"email":email,
			"password": password
		}
		$.ajax({
			url: baseURL, 
			data: JSON.stringify(obj), 
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json',
			success: function(data){
				console.log(data); 
				if (data.message == 'New user created successfully') {
					sendConfirmEmail(data.user_id);
				} else {
					$('.user-alerts').append('<span class="user-alert-detail">User already exists. Please sign in.</span>');
				}
			}
		});
	}

	function signInPost(email, password) {
		var baseURL = '/api/login'; 
		var obj = {
			"email": email,
			"password": password
		}
		console.log(obj);
		$.ajax({
			url: baseURL, 
			data: JSON.stringify(obj), 
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json',
			success: function(data){
				console.log(data);
				if (data.message == 'Successful login') {
					console.log(data);
					window.location.href="/dashboard";
				} else {
					$('.user-alerts').append('<span class="user-alert-detail">Invalid email and/or password</span>');
				}
			}
		});
	}

	function sendConfirmEmail(id) {
		var obj = {
			"user_id": id
		}
		$.ajax({
			url: '/api/confirm-email', 
			data: JSON.stringify(obj), 
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json', 
			success: function(data){
				window.location.href="/dashboard";
			}
		});
	}

	function sendPasswordResetEmail(email) {
		var obj = {
			"email": email
		}
		$.ajax({
			url: '/api/forgot-password', 
			data: JSON.stringify(obj), 
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json', 
			success: function(data){
				console.log(data.message);
				$('.forgot-password-form').addClass("hidden");
				$('.forgot-password-confirmation').removeClass("hidden");
			}
		});
	}

	////Event listeners
	//Click Sign In Toggle//
	$(".sign-in-link").click(function(event){
		$('.join-main').addClass("hidden");
		$('.sign-in-main').removeClass("hidden");
		$('.user-alert-detail').remove();
	});	
	//Click join link 
	$(".join-link").click(function(event){
		$('.sign-in-main').addClass("hidden");
		$('.join-main').removeClass("hidden");
		$('.user-alert-detail').remove();
	});

	//Submit Join Form 
	$(".join-form").submit(function(event){
		event.preventDefault();
		$('.user-alert-detail').remove();
		var firstName = $('#first-name').val();
		var lastName = $('#last-name').val();
		var email = $('#email').val();
		var password = $('#password').val();
		joinPost(firstName, lastName, email, password);
	});

	//Submit Sign In Form 
	$(".sign-in-form").submit(function(event){
		event.preventDefault();
		$('.user-alert-detail').remove();
		var email = $('#sign-in-email').val();
		var password = $('#sign-in-password').val();
		console.log(email + password);
		signInPost(email, password);
	});

	//Click forgot password
	$(".forgot-password").click(function(event){
		$(".forgot-password-form").removeClass("hidden");
	});

	//Click cancel forgot password
	$(".forgot-password-cancel-button").click(function(event){
		$(".forgot-password-form").addClass("hidden");
	});

	//Click send password reset email 
	$(".forgot-password-submit-button").click(function(event){
		var email = $('#forgot-password-email').val();
		sendPasswordResetEmail(email);
	})
});

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
					window.location.href="/dashboard";
				} else {
					$('.join-form').prepend('<span>User already exists. Please log in</span>');
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
				if (data.message == 'Successful login') {
					console.log(data);
					window.location.href="/dashboard";
				} else {
					$('.sign-in-form').prepend('<span>Invalid email and/or password</span>');
				}
			}
		});
	}


	////Event listeners
	//Click Sign In Toggle//
	$(".sign-in-link").click(function(event){
		$('.join-main').addClass("hidden");
		$('.sign-in-main').removeClass("hidden");
	});	
	//Click join link 
	$(".join-link").click(function(event){
		$('.sign-in-main').addClass("hidden");
		$('.join-main').removeClass("hidden");
	});

	//Submit Join Form 
	$(".join-form").submit(function(event){
		event.preventDefault();
		var firstName = $('#first-name').val();
		var lastName = $('#last-name').val();
		var email = $('#email').val();
		var password = $('#password').val();
		joinPost(firstName, lastName, email, password);
	});

	//Submit Sign In Form 
	$(".sign-in-form").submit(function(event){
		event.preventDefault();
		var email = $('#sign-in-email').val();
		var password = $('#sign-in-password').val();
		console.log(email + password);
		signInPost(email, password);
	});
});

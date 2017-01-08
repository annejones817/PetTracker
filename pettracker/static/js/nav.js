$(document).ready(function(event){
	//function to check log in status
	function checkLogin(){
		$.ajax({
			url: '/api/check-login', 
			type: 'GET',
			contentType: 'application/json',
			success: function(data){
				if (data.message == 'Logged in') { 
					$('.nav-link-logged-out').addClass("hidden"); 
				} else {
					$('.nav-link-logged-in').addClass("hidden");
				}
			}

		});
	}

	//check for log in on page load
	checkLogin(); 
});
$(document).ready(function(){

	//Toggle Sign In/Join
	function toggleSignInJoin(){
		signInInterface = $(".join-sign-in-main");
		signInInterface.toggleClass('js-join');
		if (signInInterface.hasClass('js-join')) {
			$(".sign-in-headline").text("Get Started With PetTracker");
			$(".sign-in-link").text("Sign In");
			$(".join-sign-in-toggle-question").text("Already a member?");
			$(".name").removeClass("hidden");
			$(".join-sign-in-button").text("Join PetTracker");
			
		} else {
			$(".sign-in-headline").text("Welcome back!");
			$(".sign-in-link").text("Join Now");
			$(".join-sign-in-toggle-question").text("Need an account?");
			$(".name").addClass("hidden");
			$(".name-entry").removeAttr("required");
			$(".join-sign-in-button").text("Sign In");

			
		}
	}

	////Event listeners
	//Click Join Sign In Toggle//
	$(".sign-in-link").click(function(event){
		toggleSignInJoin();
	});	
	//Submit Sign In Form 
	$(".js-sign-in-form").submit(function(event){

	});
});

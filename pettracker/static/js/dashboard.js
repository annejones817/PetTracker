$(document).ready(function(){
	//Get pet data
	//Testing New
	function getPetData (callback){
		var baseURL = '/api/pets';
		$.getJSON(baseURL, callback);
	}	

	function generateResultsHTML(data){
		var petCardsHTML = '';
		var petTrackerHTML = '';
		if (data.length >= 1) {
			for (var i=0; i<data.length; i++) {	
				petCardsHTML += 
					'<div class="pet-card col-3">' +
						'<h2 class="pet-card-name" id="' + data[i].id + '">' + data[i].name + '</h2>' +
						'<img class="pet-photo pet-photo-' + data[i].id + '"/>' + 
						'<div class="dashboard-pet-buttons">' +
						'<button class="pet-card-details-button" id="more-details/' + data[i].id + '">More Details</button>' +
						'<button class="delete-pet" id="delete-pet/' + data[i].id + '">Delete Pet</button>' +
						'</div>' +
					'</div>';

				petTrackerHTML +=
					'<div class="pet-tracker-details">' +
						'<h2 class="pet-tracker-name">' + data[i].name + '</h2>' +
						'<div class="pet-tracker-details-container-' + data[i].id + '"></div>' +
					'</div>';
			}		
			$('.pets-container').prepend(petCardsHTML);	
			$('.pettracker-container').append(petTrackerHTML);		
		} else {
			$('.pettracker-headline').text('Add a pet to get started.')
		}
	}

///Functions for populating pet photos
	function populatePetPhotos(data) {
		for (var i=0; i<data.length; i++) {
				var petID = data[i].id;
				getPetPhoto(petID);
			}	
	}

	function getPetPhoto(petID) {
		var baseURL = 'api/get-photo/' + petID; 
		$.ajax({
			url: baseURL, 
			dataType: 'json',
			type: 'GET',
			contentType: 'application/json',
			success: function(data){
				if (data) {
					updatePetPhoto(data);
				} else {
					console.log('fail');
				}
			}
		});
	}

	function updatePetPhoto(data) {
		var photoSrc = 'photos/paw-print.png';
		if (data.message != "No photo") {
			photoSrc = 'photos/' + data.src[0];
		}
		$('.pet-photo-' + data.id).attr('src', photoSrc);

	}

////Functions for populating pettracker details
	function populatePetTracker(data){
		console.log("populate running");
		for (var i=0; i<data.length; i++) {
			var petID = data[i].id;
			getPetTrackerDetails(petID);

		}
	}

	function getPetTrackerDetails(petID) {
		console.log("get details running");
		var baseURL = '/more-details/api/more-details/' + petID; 
		$.ajax({
			url: baseURL, 
			dataType: 'json', 
			type: 'GET', 
			contentType: 'application/json',
			success: function(data){
				if (data) {
					updatePetTracker(data);
				} else {
					console.log('fail');
				}
			}
		});
	}

	function updatePetTracker(data){
		var petID = data["pet"]["id"];
		var petTrackerDetailsHTML = '';
		var petBirthdate = data["pet"]["birthdate"];
		///manipulations to petBirthdate
		var petAge = moment().diff(petBirthdate, 'years', false);
		var formattedBirthdate = moment(petBirthdate).format("MMMM D");
		///Add birthday related details
		petTrackerDetailsHTML += '<div class="pet-tracker-detail birthday">Birthday: ' + formattedBirthdate + '</div>' +
		'<div class="pet-tracker-detail birthday">Age: ' + petAge + ' year(s)</div>';
		$('.pet-tracker-details-container-' + petID).append(petTrackerDetailsHTML);

	}

	function displayResults(data){
		generateResultsHTML(data);
		populatePetPhotos(data);
		populatePetTracker(data);
	}

	getPetData(displayResults);

	//Listen for more pet details click
	$('.pets-container').on('click', '.pet-card-details-button', function(event){
		var petDetailsURL = $(this).attr("id");
		window.location.href=petDetailsURL;
	});

	$('.pets-container').on('click', '.pet-card-name', function(event){
		var petDetailsURL = 'more-details/' + $(this).attr("id");
		window.location.href=petDetailsURL;
	});

});

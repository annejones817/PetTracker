$(document).ready(function(){
	//Get pet data
	//Testing New
	function getPetData (callback){
		var baseURL = '/api/pets';
		$.getJSON(baseURL, callback);
	}	

	function generateResultsHTML(data){
		console.log(data);
		var petCardsHTML = '';
		var petTrackerHTML = '';
		if (data.length >= 1) {
			for (var i=0; i<data.length; i++) {
				petCardsHTML += 
					'<div class="pet-card col-3">' +
						'<h2 class="pet-card-name">' + data[i].name + '</h2>' +
						//'<span class="upload-pet-photo" id="pet-photo/' + data[i].id +'">Upload Photo</span>' + 
						'<button class="pet-card-details-button" id="more-details/' + data[i].id + '">More Details</button>' +
						'<button class="delete-pet" id="delete-pet/' + data[i].id + '">Delete Pet</button>' +
					'</div>'

				petTrackerHTML +=
					'<div class="pet-tracker-details">' +
						'<h2 class="pet-card-name">' + data[i].name + '</h2>' +
					'</div>'	
					
			}
		} else {
			$('.pettracker-headline').text('Add a pet to get started.')
		}
		console.log()
		$('.pets-container').prepend(petCardsHTML);	
		$('.pettracker-container').append(petTrackerHTML);
	}

	function displayResults(data){
		generateResultsHTML(data);
	}

	getPetData(displayResults);

	//Listen for more pet details click
	$('.pets-container').on('click', '.pet-card-details-button', function(event){
		var petDetailsURL = $(this).attr("id");
		window.location.href=petDetailsURL;
	});

});

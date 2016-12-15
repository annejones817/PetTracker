$(document).ready(function(){
	//Get pet data
	//Reset again
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
						'<h2 class="pet-card-name">' + data[i].name + '</h2>' +
						'<button class="pet-card-details-button">More Details</button>' 	
					'</div>'
				petTrackerHTML +=
					'<div class="pet-tracker-details">' +
						'<h2 class="pet-card-name">' + data[i].name + '</h2>' +
					'</div>'	
					
			}
		} else {
			$('.pettracker-headline').text('Add a pet to get started.')
		}
		$('.pets-container').prepend(petCardsHTML);	
		$('.pettracker-container').append(petTrackerHTML);
	}

	function displayResults(data){
		generateResultsHTML(data);
	}

	getPetData(displayResults);

});

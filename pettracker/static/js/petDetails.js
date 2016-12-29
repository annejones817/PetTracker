$(document).ready(function(){

	//variables to store pet details
	var name; 
	var birthdate; 
	var vetName; 
	var vetPhone; 
	var vetEmail;
	var foodName; 
	var cupsPerDay;

	//Get pet details
	function getDetails(petDetailsPath) {
			var baseURL = 'api' + petDetailsPath; 
			$.ajax({
				url: baseURL, 
				dataType: 'json',
				type: 'GET',
				contentType: 'application/json',
				success: function(data){
					if (data) {
						console.log(data);
						displayDetails(data);
					} else {
						console.log("no data");
					}
				}
			});
		}

	function generateResultsHTML(data){
		var basicHTML = '';
		var medicalHTML = '';
		var foodHTML = '';
		if (data[0].name) {
			basicHTML += '<div class="pet-detail">Name: ' + data[0].name + '</div>';
			name = data[0].name;
			$('#pet-name').attr('placeholder', name);
		}
		if (data[0].birthdate) {
			birthdate = moment(data[0].birthdate).format("MMM Do YYYY");
			//birthdate = new Date(birthdate);
			//$('#datepicker').val(birthdate.getFromFormat("yyyy-mm-dd"));
			basicHTML += '<div class="pet-detail">Birthdate: ' + birthdate + '</div>';
		}
		$('.basic-pet-details-content').append(basicHTML);
		
		if (data[1]) {
			if (data[1].vet_name) {
				medicalHTML += '<div class="pet-detail">Vet Name: ' + data[1].vet_name + '</div>';
				vetName = data[1].vet_name;
			}

			if (data[1].vet_phone) {
				medicalHTML += '<div class="pet-detail">Vet Phone: ' + data[1].vet_phone + '</div>';
				vetPhone = data[1].vet_phone;
			}

			if (data[1].vet_email) {
				medicalHTML += '<div class="pet-detail">Vet Email: ' + data[1].vet_email + '</div>';
				vetEmail = data[1].vet_email;
			}
			$('.medical-pet-details-content').append(medicalHTML);
		}	

		if (data[2]) {
			if (data[2].food_name) {
				foodHTML += '<div class="pet-detail">Food Name: ' + data[2].food_name + '</div>';
				foodName = data[2].food_name;
			}

			if (data[2].cups_per_day) {
				foodHTML += '<div class="pet-detail">Cups Per Day: ' + data[2].cups_per_day + '</div>';
				cupsPerDay = data[2].cups_per_day;
			}
			$('.food-details-content').append(foodHTML);
		}	

	}

	function displayDetails(data) {
		if (data[0].name) {
			$('.pet-details-headline').text(data[0].name);		
			} else {
			$('.pet-details-headline').text('Name error');
		}
		generateResultsHTML(data);
	}

	function progressHandlingFunction(e){
	   if(e.lengthComputable){
	       $('progress').attr({value:e.loaded,max:e.total});
	   }
	}

	function editDetails(){
		$('.pet-detail').remove();
		$('.save-pet-details-button').removeClass('hidden');
		$('.pet-details-input-section').removeClass('hidden');

		//$('.edit-pet-details-row').removeClass('hidden');
	}

	function saveDetails(){
		//initialize variables
		var splitURL = window.location.href.split('/');
		var petName;
		var petBirthdate;
		var vetName;
		var vetPhone;
		var vetEmail;
		var foodName; 
		var cupsPerDay;
		var obj = {"pet-id": splitURL[4] };

		//Set variables
		
		petName = $('#pet-name').val();
		obj["pet-name"] = petName; 
		
		petBirthdate = $('#datepicker').val();
		obj["pet-birthdate"] = petBirthdate; 

		vetName = $('#vet-name').val();
		obj["vet-name"] = vetName; 

		vetPhone = $('#vet-phone').val();
		obj["vet-phone"] = vetPhone; 
		
		vetEmail = $('#vet-email').val();
		obj["vet-email"] = vetEmail; 
	
		foodName = $('#food-name').val();
		obj["food-name"] = foodName; 

		cupsPerDay = $('#cups-per-day').val();
		obj["cups-per-day"] = cupsPerDay; 

		var baseURL = '/api/update-pet';
		
		$.ajax({
			url: baseURL, 
			data: JSON.stringify(obj), 
			dataType: 'json',
			type: 'POST',
			contentType: 'application/json',
			success: function(data){
				console.log(data);
				if (data) {
					console.log("success");
					$('.edit-pet-details-row').addClass('hidden');
					getDetails(petDetailsPath);
					$('.pet-details').removeClass('hidden');
					$('.edit-pet-details-button').removeClass('hidden');
				} else {
					console.log("fail");
				}
			}
		});
	}	

	Date.prototype.getFromFormat = function(format) {
	   var yyyy = this.getFullYear().toString();
	   format = format.replace(/yyyy/g, yyyy)
	   var mm = (this.getMonth()+1).toString();
	   format = format.replace(/mm/g, (mm[1]?mm:"0"+mm[0]));
	   var dd  = this.getDate().toString();
	   format = format.replace(/dd/g, (dd[1]?dd:"0"+dd[0]));
	   var hh = this.getHours().toString();
	   format = format.replace(/hh/g, (hh[1]?hh:"0"+hh[0]));
	   var ii = this.getMinutes().toString();
	   format = format.replace(/ii/g, (ii[1]?ii:"0"+ii[0]));
	   var ss  = this.getSeconds().toString();
	   format = format.replace(/ss/g, (ss[1]?ss:"0"+ss[0]));
	   return format;
	 };
	
	//Get pet details on page load
	var petDetailsPath = window.location.pathname;
	getDetails(petDetailsPath);

	//Initialize datepicker for birthdate
	$('#datepicker').datepicker({
		dateFormat: "yy-mm-dd", 
		defaultDate: birthdate
	});	

	//Listen for Upload File
	$('#upload-file').submit(function(event){
		event.preventDefault();

	    // Create a FormData object from the upload form
	    //var data = new FormData($('form')[0]);
	    var data = new FormData();
	    var name = 'Testing';
	    data.append(name, $('form')[0], 'string');
	    console.log(data);
	    // Make a POST request to the file upload endpoint
	    var ajax = $.ajax('/api/files', {
	        type: 'POST',
	        xhr: function createUploadXhr() {
			    // XHR file upload magic
			    var xhr = new XMLHttpRequest();
			    if(xhr.upload) { // if upload property exists
			      xhr.upload.addEventListener('progress',progressHandlingFunction, false);
			    }
			    return xhr;
				},
	        data: data,
	        cache: false,
	        contentType: false,
	        processData: false,
	        dataType: 'json',
	        success: function(data) {
	        	console.log(data);
	        }

	    });
	    $('.file-upload').addClass('hidden');
	    $('.pet-details-section-records').removeClass('hidden');
	});

	//Listen for click on add record button
	$('.add-new-record-button').click(function(event){
		$('.pet-details-section-records').addClass('hidden');
		$('.file-upload').removeClass('hidden');
	});

	//Listen for click on edit details button
	$('.edit-pet-details-button').click(function(event){
		console.log('edit clicked');
		$(this).addClass('hidden');
		editDetails();
	});

	//Listen for submit save details form
	$('body').on('submit', '.edit-pet-details-form', (function(event){
		console.log("save clicked");
		event.preventDefault(); 
		saveDetails();
	}));

});

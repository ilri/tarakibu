/**
	The main file that will hold all javascript functions for the DGEA sampler
*/

var DGEA = {
   
   /**
    * The port that will be used by the system
    */
   port: undefined, 
   /**
    * Fetch all the cattle in the selected household
    */
   fetchHouseholdCattle: function(){
      if($('[name=household]').val() == 0){
         alert('Please select a household of which to fetch the cattle');
         return;
      }
      //create a request for this data
       DGEA.submitForm('simple/selectedHousehold', 'householdCattle');
   },
   
	displayCattleInHomestead: function(){
	},
   
   updateGPSCoordinates: function(){
      $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/simple/updateGPSCoordinates', data: 'page=simple', dataType: 'html', success: function(data){$('#gps_position').html(data)}});
      //keep updating the gps information
      setTimeout('DGEA.updateGPSCoordinates()', 500)
   },
   
   /**
    * Sends the defined form data to the server if the form is designed, else sends the data of the first form
    * 
    * modules: A string that defines which modules are to be executed on the server
    * field:   A string with fieldId that is meant to be updated with the results from the server
    * name:    (optional) The name of the form whose details we want sent. In case none is defined, we send the details of the first form
    */
   postForm: function(modules, field, name){
      var params;
      if(name == undefined){ //look out for the first form that needs to be sent back to the server
         params = $('form').formSerialize();
      }
      else{ //encode the contents of the named form and send them to the server
         params = $('[name='+name+']').formSerialize();
      }
	  if(typeof(modules) != 'string'){	//we have all our data here! so lets play safe
		 reqModule = modules.data.module
		 DGEA.field2Update = modules.data.field;
	  }
	  else{	//we are expecting everything as passed
		 reqModule = modules
		 DGEA.field2Update = field;
	  }
      //$.post('http://localhost:'+DGEA.port+'/'+modules, params, DGEA.updateField);
      //$.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/'+modules, data: $.toJSON(params), dataType: 'html', success:DGEA.updateField});
      $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/'+reqModule, data: params, dataType: 'html', success:DGEA.updateField});
   },
   
   /**
    * Creates an AJAX call to update the necessary component that needs updating. Expects the parameters to be passed to the server
    */
   ajaxFunction: function(params){
      if(typeof params != 'string'){
         return;     //we only expecting parameters which are strings in nature....anything else is junk to us!
      }
      var xmlhttp;
      if (window.XMLHttpRequest) {
         xmlhttp=new XMLHttpRequest();
      }
      else if (window.ActiveXObject) {
         xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
      xmlhttp.onreadystatechange=function() {
         if(xmlhttp.readyState==4) {
            eval(xmlhttp.responseText);
         }
      }
      xmlhttp.open("GET", 'http://localhost:'+DGEA.port+'/'+params, true);
      xmlhttp.send(null); 
   },
   
   updateField: function(result){
	  if(result.substr(0,2)=='-1'){
		 var message=result.substring(2,result.length);
		 DGEA.ajaxError(message);
		 return;
	  }
	  
      if(DGEA.field2Update == undefined) return;          //we dont know what to update....
      else $('#'+DGEA.field2Update).html(result);
   },
   
   /**
    * Submits the data of a form to the server. Assumes that there is only one form in a a page at a time, and if there are multiple submits only the first one
    */
   submitForm: function(vars, updateMe){
      var params = $('form').formSerialize();
      var module = (vars.data != undefined) ? vars.data.module : vars;
      DGEA.field2Update = (updateMe == undefined) ? 'main_box' : updateMe;
      $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/'+module, data: params, dataType: 'html', success:DGEA.updateField});
   },
   
   /**
    * Submits the entered sample to the server
    */
   submitSamples: function(){
	  //get the sample barcode and the extra information that is associated with this sample
	  var sample = $.trim($('#sample').val()), comments = $('#comments').val(), curAnimalRead = $('[name=curAnimalRead]').val(), curAnimal = $('[name=curAnimal]').val();
	  if(sample == ''){
		 $('#error').html("Please enter the barcode number or scan the sample!");
		 $('#sample').focus();
		 return;
	  }
	  //we have the samples and the data, now post them to the server
	  var params = 'barcode='+encodeURIComponent(sample)+'&comments='+encodeURIComponent(comments)+'&curAnimalRead='+encodeURIComponent(curAnimalRead)+'&curAnimal='+encodeURIComponent(curAnimal)+'&page=simple';
      DGEA.field2Update = 'box_main';
      $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/simple/saveSample', data: params, dataType: 'json', success:DGEA.saveSampleResult});
   },
   
   ajaxError: function(message){
      if(message == undefined) message = '';
	  $('#error').html(message);
   },
   
   saveSampleResult: function(data){
      $('#sample').val('').focus();
      setTimeout('DGEA.ajaxError()', 5000);   //clear the error message in case we have one being shown
	  if(data.error != undefined){
		 $('#error').html(data.error);
		 return;
	  }
     if(data.saved == 1){ //the sample has already been saved before and we have the data of the animal that has been saved
        DGEA.displayAnimalInfo(data);
        DGEA.ajaxError(data.mssg);
        setTimeout('DGEA.displayAnimalInfo()', 5000);   //revert to showing the current animal after some secs
        setTimeout('DGEA.ajaxError()', 5000);   //clear the error message in case we have one being shown
     }
     else{  //the sample was saved well
        DGEA.curAnimal = data;
        DGEA.displayAnimalInfo();
        //if we have a message display it
        if(data.mssg != undefined){
           $('#general').html(data.mssg);
           setTimeout('DGEA.ajaxError()', 5000);   //clear the message after 5 seconds
        }
     }
   },
   
   /**
    * We need to display the informtion about a certain animal. If no animal object is passed, display the curAnimal
    */
   displayAnimalInfo: function(animal){
      var curAnimal = (animal == undefined) ? DGEA.curAnimal : animal;
      
      var content = '';
      content += (animal == undefined) ? '<div>Current Animal Samples: <b>' : '<div>Samples for: <b>';
      content += curAnimal.animal+"</b></div><ul>";
      $.each(curAnimal.samples, function(){
         content += '<li>'+this.barcode+', '+this.sampling_date_time+" <image src='resource?images/delete.png' alt='close' class='delete_sample "+this.barcode+"' /></li>";
      });
      content += "</ul>";
      $('#info').html(content);
      $('.delete_sample').bind('click', DGEA.deleteSample);
   },
   
   /**
    * Clear the information panel that is to the right
    */
   clearInformation: function(){
      var content = "<h2>Information</h2><hr /><div class='scroller info' id='info'></div><div class='scroller general' id='general'></div><div class='scroller error' id='error'></div>";
      $('#main_info').html(content);
      DGEA.displayAnimalInfo();     //and then update the animal info
   },
   
   /**
    * Delete a sample!
    */
   deleteSample: function(){
      var barcodeRe = /^delete_sample\s(.+)$/i
      var res = barcodeRe.exec(this.className);
      if(confirm('Are you sure you want to delete ' + res[1]) == true){
         var params = 'page=simple&sample='+encodeURIComponent(res[1]);
         $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/simple/deleteSample', data: params, dataType: 'json', success:DGEA.saveSampleResult});
      }
      else return;   //we have though twice and decided not to delete the sample
   },
   
   deleteAnimal: function(){
      var animalRe = /^delete_animal\s(.+)$/i
      var res = animalRe.exec(this.className);
      //check if we have any samples associated with this animal, and only proceed if we have some samples
      if(DGEA.curAnimal.samples.length == 0){
         $('#general').html('Sorry, but the current animal does not have any samples to be deleted!');
         setTimeout('DGEA.clearInformation()', 5000);   //clear this message after 5 seconds
         return;
      }
      if(confirm('Are you sure you want to delete this animal('+res[1]+') sampling record and all the samples associated with this animal.') == true){
         var params = $('form').formSerialize();
         DGEA.field2Update = 'main_box';
         $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/simple/deleteAnimal', data: params, dataType: 'html', success:DGEA.updateField});
      }
      else return;   //we have though twice and decided not to delete the sample
   }
};
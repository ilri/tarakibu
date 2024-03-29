/**
 Copyright 2011 ILRI
 
 This file is part of tarakibu.
 
 tarakibu is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 tarakibu is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with tarakibu.  If not, see <http://www.gnu.org/licenses/>.
 
*/

/**
	The main file that will hold all javascript functions for the DGEA sampler
*/
var DGEA = {
   
   /**
    * The port that will be used by the system
    */
   port: undefined, 

   getVariable: function(name,queryStr){
   //it gets a string as the variables passed in the location and returns a variable by the specific name
      queryStr=unescape(queryStr)		//make it a proper string
      queryStr=queryStr.replace("+"," ").replace("+"," ")	//remove the +'s
       if (queryStr.length != 0) {
         splitArray = queryStr.split("&")	//convert it to an array
         for (i=0; i<splitArray.length; i++) {
            var splits=splitArray[i].split("=");
            if(splits[0]==name) return splits[1];
         }
       }
      return undefined;
   },

   /**
    * Fetch all the cattle in the selected household
    */
   fetchHouseholdCattle: function(){
      if($('[name=household]').val() == 0){
         alert('Please select a household of which to fetch the cattle.');
         return;
      }
      //create a request for this data
       DGEA.submitForm('simple/selectedHousehold', 'householdCattle');
   },
   
   /**
    * Fetch all the households in the selected site
    */
   fetchSiteHouseholds: function(){
      if($('[name=sites]').val() == 0){
         alert('Please select a site from which to fetch all the households.');
         return;
      }
      //create a request for this data
       DGEA.submitForm('simple/selectedSite', 'siteHouseholds');
   },
   
	displayCattleInHomestead: function(){
	},
   
   updateGPSCoordinates: function(){
      $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/simple/updateGPSCoordinates', data: 'page=simple', dataType: 'html', 
         success: function(data){$('#gps_position').html(data)}, 
         error: function(data){$('#gps_position').html("<div class='gps_disconnected'>Lost connection to the server.</div>")}
      });
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
        setTimeout('DGEA.ajaxError()', 5000);   //clear the error message after a while
        setTimeout('DGEA.generalMessage()', 5000);   //clear the general message after a while, if any
		 return;
	  }
	  
      if(DGEA.field2Update == undefined) return;          //we dont know what to update....
      else $('#'+DGEA.field2Update).html(result);
   },
   
   /**
    * Submits the data of a form to the server. Assumes that there is only one form in a a page at a time, and if there are multiple submits only the first one
    */
   submitForm: function(vars, updateMe){
      var params = $('form').formSerialize(), module;
      if(vars.data != undefined){
         module = vars.data.module;
         DGEA.field2Update = (vars.data.updateMe == undefined) ? 'main_box' : vars.data.updateMe;
      }
      else{
         module = vars;
         if(updateMe != undefined) DGEA.field2Update = updateMe;
         else DGEA.field2Update = 'main_box';
      }
      
      $.ajax({type: 'POST', url:'http://localhost:'+DGEA.port+'/'+module, data: params, dataType: 'html', success:DGEA.updateField, 
         error: function(){ $('#'+DGEA.field2Update).html("<div class='gps_disconnected'>Lost connection to the server.</div>"); }
      });
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
   
   generalMessage: function(message){
      if(message == undefined) message = '';
	  $('#general').html(message);
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
           setTimeout('DGEA.generalmessage()', 5000);   //clear the message after 5 seconds
        }
     }
   },
   
   /**
    * We need to display the informtion about a certain animal. If no animal object is passed, display the curAnimal
    */
   displayAnimalInfo: function(animal){
      var curAnimal = (animal == undefined) ? DGEA.curAnimal : animal;
      if(curAnimal.animal == undefined) return;
      
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
      else{ return; }   //we have though twice and decided not to delete the sample
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
      else{ return; }  //we have though twice and decided not to delete the sample
   },
   
   changedRadius: function(){
      //get the current value and see if it has changed in any way, if it has get the new households
      var curRadius = $('[name=radius]').val();
      if(curRadius == DGEA.curRadius) return;
      
      //remove the current data
      $('#siteHouseholds').html("<div class='error'>Updating</div>");
      //create a request for this data
       DGEA.submitForm('simple/updateHouseholds', 'siteHouseholds');
       $('#householdCattle').html("<select><option value='0'>Select One</option></select>");
   },
   
   /**
    * Refresh the page as it is....this will be crazy!!
    */
   refreshPage: function(){
      //we want to refresh the page
      var div2update = '', radius = undefined, household = undefined, cow2sample = undefined, curAnimal = undefined, site = undefined, sample = undefined;
      var curAnimalReadId = undefined;
      
      if($('[name=household]').length != 0) household = $('[name=household]').val();
      if($('[name=site]').length != 0) site = $('[name=site]').val();
      if($('[name=cow2sample]').length != 0) cow2sample = $('[name=cow2sample]').val();
      if($('[name=curAnimal]').length != 0) curAnimal = $('[name=curAnimal]').val();
      if($('[name=sample]').length != 0) sample = $('[name=sample]').val();
      if($('[name=curAnimalRead]').length != 0) curAnimalReadId = $('[name=curAnimalRead]').val();
      if($('[name=radius]').length != 0) radius = $('[name=radius]').val();
      
//      var household = $('[name=household]').val();
//      var household = $('[name=household]').val();
//      var household = $('[name=household]').val();
      if(household != 0 && cow2sample == 0) div2update = 'householdCattle';
      else if(radius != undefined && household != 0) div2update = 'siteHouseholds';      //update the household in the given radius
      DGEA.submitForm('simple/refreshSampler', div2update);
   }
};

var paged = DGEA.getVariable('page',document.location.search.substring(1));
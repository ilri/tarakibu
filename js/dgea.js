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
       DGEA.ajaxFunction('simple/selectedHousehold');
   },
   
	displayCattleInHomestead: function(){
	},
   
   updateSite: function(module){
      /**
       * i think ajaxfunction is called with different parameters depending on the page which was loaded....
       * The admin page is loaded with 'admin/update'
       * The site page is loaded with 'site/update', 'site/previous_samples'
       */
      if(module == 'simple'){
         DGEA.ajaxFunction('simple/update');
      }
      else{
         DGEA.ajaxFunction('http://localhost:%s/','site/update');
         DGEA.ajaxFunction('http://localhost:%s/','site/location');
      }
      //keep updating the gps information
      setTimeout('DGEA.updateSite("'+module+'")', 500)
   },
   
   /**
    * Sends the defined form data to the server if the form is designed, else sends the data of the first form
    */
   postForm: function(name){
      if(typeof name == undefined){ //look out for the first form that needs to be sent back to the server
         
      }
      //$.()
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
   }
};
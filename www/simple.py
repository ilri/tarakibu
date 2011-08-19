"""
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
 
"""

import json
from common import *
from time import time, sleep

errors = {'label':'Could not verify tag label. Verify that this animal is part of the sampling process and try again',
          'unknown_tag':'The tag you have input is not featured in the animal database. This animal is not part of the sampling program.',
          'invalid_barcode':'Already scanned or not a valid barcode',
          'animal_no_gps':'Cannot input tag read without gps position.',
          'invalid_gps':'The current GPS coordinates are not valid. Please wait until you get a valid GPS coordinate and then try again.',
          'sample_no_gps':'Cannot input sample without gps position.'}


class simple(SimplePage):
    """
    Description of this class!
    """
    
    def curPosition(self, gps):
        """
        We want the current GPS position
        """
        #print self.info
        return gpsPosition(gps)


    def site(self, info, gps):
        """
        Creates the initial page that will be displayed on launching dgea sampler
        """
        return """<html>
            <head>
              <title>%s v. %s</title>
              <script type='text/javascript' src='resource?js/jquery_1_6_1.js'></script>
              <script type='text/javascript' src='resource?js/dgea.js'></script>
              <script type='text/javascript' src='resource?js/jquery.json.js'></script>
              <script type='text/javascript' src='resource?js/jquery.form.js'></script>
              <link rel='stylesheet' type='text/css' href='resource?css/dgea.css'>
              <script type='text/javascript'>
                  //set the port that will be used on the js side
                  DGEA.port = %s;
                  //call the updateSite function once the page is fully loaded
                  $(document).ready(function() {
                      DGEA.updateGPSCoordinates();            //start the process of getting streaming GPS coordinates
                  });
              </script>
            </head>
            <body>
              <div class='site'>
                  <div class='left'>
                      <div class='box top'>
                          <h1><a href='http://localhost:%s/'>%s</a></h1>
                      </div>
                      <div class='box main' id='main_box'>
                        <div><h2>DGEA Sampling</h2><a href='javascript:DGEA.refreshPage()'><img class='refresh' src='resource?images/refresh.png' alt='Refresh' /></a><hr /></div>
                        <form method='post' enctype='multipart/form-data' name='sampling'>
                          <input type='hidden' name='page' value='simple'>
                          <div class='scroller input' id='input_form'>%s</div>
                        </form>
                      </div>
                  </div>
                  <div class='right'>
                      <div class='box top'>
                          <table>
                              <tr><td>GPS:</td><td id='gps_position'>&nbsp;</td></tr>
                          </table>
                      </div>
                  <div id='main_info' class='box main'>
                      <h2>Information</h2>
                      <hr />
                      <div class='scroller info' id='info'></div>
                      <div class='scroller general' id='general'></div>
                      <div class='scroller error' id='error'></div>
                  </div>
              </div>
              <div class='footer'>
                  <a href='/admin'>< Administration page</a> * %s v. %s. &copy; AVID Team, AVID Project, ILRI, 2010 * <a href='/summary'>Sampling Summary >></a>
              </div>
            </div>
              <script type='text/javascript'>
                  $('[name=submit]').bind('click', {module: 'simple/dgea_form'}, DGEA.submitForm);
              </script>
            </body>
          </html>
          """ % (self.title, self.version, self.port, self.port, self.title, self.dgeaHome(gps), self.title, self.version)


    def dgeaHome(self, gps, showAllSites = 0, curAnimalRead = 0, radius = 0):
        """
        Creates the home page of the DGEA sampler
        
        @todo add a slider that will change the radius of the households that are being displayed on the fly
        """
        checked = 'checked' if (showAllSites == 1) else ''

        curSiteId = 0
        radius = self.radius if radius == 0 else radius;
        curHouseholdId = 0
        householdCattle = "<tr><td>Cattle ID:</td><td id='householdCattle'><select name='cow2sample'><option value='0'>Select One</option></select></td></tr>"    #the combo for the cattle when we have none
        if(curAnimalRead != 0):
            #we are just from sampling one animal from some site/household....for continuity sake, re-select the current site or household
            self.db.curQuery = "SELECT c.id as hhId, c.siteId FROM `animal_reads` as a inner join animals as b on a.animalid=b.id inner join households as c on b.hhId=c.id where a.id=%s" % curAnimalRead
            try:
                res = self.db.dictQuery()
                curSiteId = res[0]['siteId']
                curHouseholdId = res[0]['hhId']
                #since we have the household, get all the animals from this household
                householdCattle = "<tr><td>Cattle ID:</td><td id='householdCattle'>%s</td></tr>" % self.householdCattle(curHouseholdId, gps)
            except:
                #print "Error while fetching the site id and household id of the current animal read" + self.db.curQuery
                return 'There was an error while fetching the site id and household id of the current animal read from the database. Please try again. If the problem persists, please restart the simple sampler.'
            #print 'curSiteId: %s, curHouseholdId: %s ' % (curSiteId, curHouseholdId)
            
        if(showAllSites == 1):
            content = """
                <table>
                <tr class='first_row'><td colspan='2'>Select a cow to sample<span class='show_all'>All sites <input type='checkbox' name='show_all' %s /></span></td></tr>
                <tr><td>Sites:</td><td><select name='sites'>%s</select></td></tr>
                """ % (checked, self.allSites(curSiteId))

            if(curAnimalRead != 0):
                #we have just sampled some animal, so re-select the previous household
                content += """
                    <tr><td>Household ID:</td><td id='siteHouseholds'><select name='household'><option value='0'>Select a Household</option>%s</select></td></tr>
                    """ % self.allHouseholds(curHouseholdId)
            else:
                #we have no household....we starting from a clean slate
                content += "<tr><td>Household ID:</td><td id='siteHouseholds'><select name='household'><option value='0'>Select a Household</option></select></td></tr>"
        else:
            content = """
                <table>
                <tr class='first_row'><td colspan='2'>
                    Select a cow to sample<span class='show_all'>Rad: <input type='text' name='radius' value='%s' size=2 /> Km.&nbsp;All sites <input type='checkbox' name='show_all' %s /></span>
                </td></tr>
                <tr><td>Household ID:</td><td id='siteHouseholds'>%s</td></tr>
                <script type='text/javascript'>
                    $('[name=radius]').bind('blur', DGEA.changedRadius);
                    DGEA.curRadius = %s;
                </script>
                """ % (radius, checked, self.householdsWithinRadius(gps, curHouseholdId), radius)
            
        content += """
            %s
            </table>
            <script type='text/javascript'>
                $('[name=household]').bind('change', DGEA.fetchHouseholdCattle);
                $('[name=sites]').bind('change', DGEA.fetchSiteHouseholds);
                $('[name=show_all]').bind('change', {updateMe: 'input_form', module: 'simple/showAllSites'}, DGEA.submitForm);
            </script>
            """ % householdCattle
        return content


    def allHouseholds(self, curHouseholdId = 0):
        """
        Create a select component for the household
        """
        output = ''
        for household in self.db.getHouseholds():
            output += '<option value=\'%s\'' % household[1]
            output += ' selected' if (household[1] == curHouseholdId) else ''
            output += '>%s</option>' % household[0]
        return output


    def householdsWithinRadius(self, gps, curHouseholdId = 0, radius = 0):
        """
        Selects all the households that fall within a given radius from the current location
        """
        while(gps.status != 'running'):
            #print 'Waiting to get a gps fix before proceeding!'
            sleep(0.5)
        radius = self.radius if radius == 0 else radius
        output = "<select name='household'><option value='0'>Select a Household</option>"
        for household in self.db.getHouseholds():
            #print gps.data['latitude']
            distance = gps.haversine(gps.data['latitude'], float(household[2]), gps.data['longitude'], float(household[3]))
            if(distance < radius):
                output += '<option value=\'%s\'' % household[1]
                output += ' selected' if (household[1] == curHouseholdId) else ''
                output += ">%s</option>\n" % household[0]
        output += '</select>'
        return output


    def allSites(self, curSiteId = 0):
        """
        Create a select component for the sites
        """
        output = "<option value='0'>Select One"
        for site in self.db.getSites():
            output += '<option value=\'%s\'' % site[0]
            output += ' selected' if (site[0] == curSiteId) else ''
            output += '>%s</option>' % site[1]
        return output


    def selectedHousehold(self, householdId, gps):
        #print 'we here'
        if gps.status == 'running':
            return self.householdCattle(householdId, gps)
        else:
            #print errors['invalid_gps']
            return '-1%s' % errors['invalid_gps']


    def selectedSite(self, siteId, gps):
       #print 'we here...want to get the households in a site'
        if gps.status == 'running':
            return self.siteHouseholds(siteId, gps)
        else:
            #print errors['invalid_gps']
            return '-1%s' % errors['invalid_gps']


    def householdCattle(self, householdId, gps):
        """
        Do the necessary checks for this household and then select all the cattle from this household
        """
        #check that the current location of this household falls within the radius of where we expect it to be
        if gps.status != 'running':
            #print errors['invalid_gps']
            return '-1%s' % errors['invalid_gps']
        
        #seems all is ok, get all the animals associated with this household
        cattleInHousehold = self.db.getHouseholdCattle(householdId)
        #logger.info("Requested for cattle in household no: %s" % householdId)
        #now lets create the dropdown for the animals
        output = "<select name='cow2sample'><option value='0'>Select One</option>"
        for cow in cattleInHousehold:
            output += "<option value='%s'>%s</option>" % (cow[0], cow[1])
        output += """
                    </select>
                    <script type='text/javascript'>
                        $('#dgea_sampling').bind('click', DGEA.ajaxFunction);
                        $('[name=cow2sample]').bind('change', {module: 'simple/sampleCow', field: 'main_box'}, DGEA.postForm);
                    </script>
                """
        return output


    def siteHouseholds(self, siteId, gps):
        """
        Do the necessary checks for this site and then select all the households from this site
        """
        #check that the current location of this household falls within the radius of where we expect it to be
        if gps.status != 'running':
            #print errors['invalid_gps']
            return '-1%s' % errors['invalid_gps']
        
        #seems all is ok, get all the animals associated with this household
        householdsInSite = self.db.getSiteHouseholds(siteId)
        #print 'going on'
        #logger.info("Requested for cattle in household no: %s" % householdId)
        #now lets create the dropdown for the animals
        output = "<select name='household'><option value='0'>Select a Household</option>"
        for site in householdsInSite:
            output += "<option value='%s'>%s</option>" % (site[1], site[0])
        output += """
                    </select>
                    <script type='text/javascript'>
                        $('[name=household]').bind('change', DGEA.fetchHouseholdCattle);
                    </script>
                """
        return output


    def collectSample(self, postvars, gps):
        """
        We are now ready to start the sample collection. We have the household where we sampling and the animal that we want sampled.
        
        Logging this event to the database and then we create the form that will be used to collect the data
        """
        #print 'sampling a cow'
        if gps.status != 'running':
            return '-1%s' % errors['invalid_gps']
        #log the gps data that we are going to link to this animal read
        gpsId = self.db.logGpsData(gps.data)
        
        #pass the variable of whether we showing all or its just a specific site
        
        #add the animal read instance to the database
        try:
            curAnimalRead = self.db.logAnimalRead(gpsId, postvars['cow2sample'][0], 'adding')
        except:
            #print 'Serious error while adding the animal read to the database.'
            return """
                <div><h2>DGEA Sampling</h2><a href='javascript:DGEA.refreshPage()'><img class='refresh' src='resource?images/refresh.png' alt='Refresh' /></a><hr /></div>
                <form method='post' enctype='multipart/form-data' name='sampling'>
                    <input type='hidden' name='page' value='simple'>
                    <div class='scroller input' id='input_form'>%s</div>
                </form>
                <script>
                    $('#error').html('There was an error while adding data to the database. Please try again and if the problem persists, please restart simple sampler.');
                    setTimeout('DGEA.clearInformation()', 5000);
                </script>
            """ % self.dgeaHome(gps)
        
        #now get the details of the animal that we are sampling
        query = 'select a.name as animalName, b.hhid, c.name as siteName from animals as a inner join households as b on a.hhId = b.id inner join sites as c on b.siteId = c.id where a.id=%s' % postvars['cow2sample'][0]
        res = self.db._query(query)
        res = res[0]
        curAnimal = res[2] + ', ' + res[1] + ', ' + res[0]
        return self.samplingPage(curAnimal, curAnimalRead, postvars)


    def samplingPage(self, curAnimal, curAnimalRead, postvars):
        """
        Creates the page to allow the user to start scanning the samples
        """
        #print 'current animal - %s' % curAnimal
        #print 'current animal read - %s' % curAnimalRead
        #get all the samples associated with this animal
        allSamples = self.animalSamples(postvars['cow2sample'][0])
        if isinstance(allSamples, str):
            return '-1%s' % allSamples
        #print allSamples
        showall = 1 if ('show_all' in postvars) else 0
        radius = "<input type='hidden' name='radius' value='%s' />" % postvars['radius'][0] if ('radius' in postvars) else ''
        #print showall
        
        return """
            <div><h2>DGEA Sampling</h2><a href='javascript:DGEA.refreshPage()'><img class='refresh' src='resource?images/refresh.png' alt='Refresh' /></a><hr /></div>
            <form method='post' enctype='multipart/form-data' name='sampling'>
                <input type='hidden' name='page' value='simple'>
                Current Animal: <b>%s</b>&nbsp;<image src='resource?images/delete.png' alt='close' class='delete_animal %s' />
                <hr />
                <table>
                <tr> <td>Sample tube:</td> <td><input type='text' name='sample' id='sample'>  </td> </tr>
                <tr> <td>Information:</td> <td><input type='text' name='comments' id='comments'></td> </tr>
                <input type='hidden' name='curAnimalRead' value='%s' />
                <input type='hidden' name='curAnimal' value='%s' />
                <input type='hidden' name='showall' value='%s' />
                %s
                </table>
                <hr />
                <a href='javascript:;' id='next_animal'>Next Animal</a>
                <script type='text/javascript'>
                    $('#next_animal').bind('click', {module: 'simple/nextAnimal', field: 'main_box'}, DGEA.submitForm);
                    $('[name=sample]').focus();
                    //bind the return key
                    $('#sample').keyup(function(e){
                        if (e.keyCode == 13) { 
                           DGEA.submitSamples();
                           return false;
                        }
                    });
                    DGEA.curAnimal = %s;
                    DGEA.displayAnimalInfo();
                    $('.delete_animal').bind('click', DGEA.deleteAnimal);
                </script>
            </form>
            """ %  (curAnimal, curAnimal, curAnimalRead, curAnimal, showall, radius, json.dumps({'animal': curAnimal, 'samples': allSamples}))


    def saveSample(self, postvars, gps, barcodedSamples):
        """
        We are adding a sample to a cow which was selected before
        
        @todo sanitize the comments
        @todo change the status of a sample read to re-sampled if the user specified a sample which is already in the database
        """
        if gps.status != 'running':
            return json.dumps({'error': "The current GPS coordinates are not valid. Please wait until you get a valid GPS coordinate and then try again."});
            
        errorMessage = {'error': 'There was an error while adding the sample to the database. Please try again. If the problem persists, please restart the simple sampler.'}
        barcode = postvars['barcode'][0].upper()
        curAnimal = postvars['curAnimal'][0]
        #check if this sample has been added before
        res = self.isSampleSaved(barcode)
        #print res
        if isinstance(res, str):    #an error occured while checking whether the sample has been saved before
            return json.dumps({'error': res})
        elif isinstance(res, dict):    #we have an array, meaning that the sample has bee saved before
            #print 'saved already'
            return json.dumps(res)

        #lets save this sample, but first get the animalId
        try:
            query = 'select animalId from animal_reads where id=%s' % postvars['curAnimalRead'][0]
            res = self.db._query(query)
        except:
            #print 'Error while fetching animal id from the database: %s' % query
            return json.dumps(errorMessage)
        
        curAnimalId = res[0][0]
        #Lets do the necessary data checks
        if (barcodedSamples == 'yes'): #we have barcoded samples, so check whether we have a good barcode as per the defined barcodes in the database
            if (self.db.isBarcodePrefixDefined(barcode) == 1):
                return json.dumps({'error': 'Invalid barcode prefix! The barcode prefix is not defined.'})
            barcodeRe = re.compile('[^0-9]{5,6}$')
            if barcodeRe.match(barcode):
                return json.dumps({'error': 'Invalid sample barcode! The entered barcode is not valid.'})
        #log this sample read
        #log the gps data that we are going to link to this animal read
        if gps.status != 'running':
            return json.dumps({'error': "The current GPS coordinates are not valid. Please wait until you get a valid GPS coordinate and then try again."});
        gpsId = self.db.logGpsData(gps.data)
        try:
            self.db.logSampleRead(barcode, gpsId, 'added')
        except:
            #print 'Error while adding a sample read.'
            return json.dumps(errorMessage)

        #we are now all set...so lets proceed to the db stuff
        try:
            query = "insert into samples(barcode, gps_id, animalReadId, animalId, comment) values('%s', %s, '%s', '%s', '%s')" % (barcode, gpsId, postvars['curAnimalRead'][0], curAnimalId, postvars['comments'][0],)
            self.db._query(query)
        except:
            #print 'Error while logging in the sample: %s' % query
            return json.dumps(errorMessage)
        #we are ok, return all the samples from this animal
        self.db.curQuery = 'select b.*, c.read_time from animal_reads as a inner join samples as b on a.animalId=b.animalId inner join gps_data as c on b.gps_id=c.id where a.id=%s' % postvars['curAnimalRead'][0]
        try:
            samples = self.db.dictQuery()
            allSamples = []
            for sample in samples:
                allSamples.append({'barcode': sample['barcode'], 'sampling_date_time': str(sample['read_time'])})
        except:
            #print 'There was an error while fetching samples: %s' % self.db.curQuery
            return json.dumps(errorMessage)
        #we are now home and dry...return the results  postvars['curAnimalRead'][0]
        return json.dumps({'animal': curAnimal, 'samples': allSamples})


    def isSampleSaved(self, barcode):
        """
        Checks whether a sample with the passed barcode has been saved or not
        
        @return     Returns 0 if it is not saved, else it returns an array with the animal metadata to which the sample belongs to, and the other samples from the same animal
        """
        self.db.curQuery = "select animalId from samples as a where barcode='%s'" % barcode
        try:
            res = self.db.dictQuery()
        except:
            #print "Error while checking if a sample exists. " + self.db.curQuery
            return "Error! There was an error while saving the sample. Please try again and if the error persists, please contact the system administrator."
        
        if (len(res) != 0):
            #this sample has already been added before, so lets get the animal to which this sample belongs
            animalDetails = self.animalDisplayName(res[0]['animalId'])
            if isinstance(animalDetails, str):
                return animalDetails
            animalDetails = animalDetails['animalName']
            
            #now lets get all the samples which have been bled from this animal
            allSamples = self.animalSamples(res[0]['animalId'])
            if isinstance(allSamples, str):
                return allSamples
            addMssg = "The sample '%s' has already been saved before." % barcode
            return {'animal': animalDetails, 'samples': allSamples, 'mssg': addMssg, 'saved': 1, 'animalId': res[0]['animalId']}
        else:
            return 0


    def nextAnimal(self, postvars, gps):
        """
        We have finalized sampling one animal, now we need to save the current samples and move to the next animal
        """
        #print 'here we are'
        if gps.status != 'running':
            return '-1%s' % errors['invalid_gps']
        radius =int(postvars['radius'][0]) if ('radius' in postvars) else 0
        #All the samples have been already saved...jst show the home page again
        return """
            <div><h2>DGEA Sampling</h2><a href='javascript:DGEA.refreshPage()'><img class='refresh' src='resource?images/refresh.png' alt='Refresh' /></a><hr /></div>
            <form method='post' enctype='multipart/form-data' name='sampling'>
                <input type='hidden' name='page' value='simple'>
                <div class='scroller input' id='input_form'>%s</div>
            </form>
            <script type='text/javascript'>
                DGEA.curAnimal = {};
                DGEA.clearInformation();
            </script>
        """ % self.dgeaHome(gps, int(postvars['showall'][0]), int(postvars['curAnimalRead'][0]), radius)


    def animalSamples(self, animalId):
        """
        Gets all the samples that have been saved from this animal
        """
        errorMessage = 'There was an error while fetching animal samples data from the database. Please try again. If the problem persists, please restart the simple sampler.'
        self.db.curQuery = "select b.read_time, a.barcode from samples as a inner join gps_data as b on a.gps_id=b.id where a.animalId = %s" % animalId
        try:
            samples = self.db.dictQuery()
            allSamples = []
            for sample in samples:
                allSamples.append({'barcode': sample['barcode'], 'sampling_date_time': str(sample['read_time'])})
        except:
            #print "Error while fetching samples associated with a certain animal. " + self.db.curQuery
            return errorMessage
        #we all good, return the samples
        return allSamples


    def animalDisplayName(self, animalId):
        """
        Get the full name of this animal. By the full name we mean the name of the animal that we are going to display
        """
        self.db.curQuery = 'select a.name as animalName, b.hhid, c.name as siteName from animals as a inner join households as b on a.hhId = b.id inner join sites as c on b.siteId = c.id where a.id=%s' % animalId
        try:
            animal = self.db.dictQuery()
            animalDetails = animal[0]['siteName'] + ', ' + animal[0]['hhid'] + ', ' + animal[0]['animalName']
        except:
            #print "Error while fetching the animal full name" + self.db.curQuery
            return 'There was an error while fetching the animal full name from the database. Please try again. If the problem persists, please restart the simple sampler.'
        return {'animalName': animalDetails}


    def deleteSample(self, sample, gps):
        """
        The user wants this sample deleted. We are going to delete it from the samples records, but add this entry into the sample reads table
        
        Returns a json object with the current animal information in case all went successfully, else it returns a json with the error
        """
        errorMessage = {'error': 'There was an error while deleting the sample from the database. Please try again. If the problem persists, please restart the simple sampler.'}
        if gps.status != 'running':
            return json.dumps({'error': errors['invalid_gps']})
        #jst for the sakes of it, lets ensure that the sample is actually sampled
        res = self.isSampleSaved(sample)
        if res == 0:
            mssg = "Error, Trying to delete '%s'. We actually do not have this sample." % sample
            return json.dumps({'error': mssg})
        #we actually have the sample, so lets delete it
        
        
        #log the gps data that we are going to link to this animal read
        gpsId = self.db.logGpsData(gps.data)
        #log this sample delete
        try:
            self.db.logSampleRead(sample, gpsId, 'deleted')
        except:
            return json.dumps(errorMessage)
        #the actual delete
        query = "delete from samples where barcode = '%s'" % sample
        self.db._query(query)
        msg = "The sample '%s' has been deleted succesfully!" % sample
        
        #now get the other samples for this animal
        allSamples = self.animalSamples(res['animalId'])
        if isinstance(allSamples, str):
            return json.dumps({'error': allSamples})
            
        #get the animal display name
        animalDetails = self.animalDisplayName(res['animalId'])
        if isinstance(animalDetails, str):
            return animalDetails
        animalName = animalDetails['animalName']
        return json.dumps({'animal': animalName, 'samples': allSamples, 'mssg': msg})


    def deleteAnimal(self, curAnimalRead, gps):
        """
        Deletes a sampled animal and also deletes all the samples associated with the current sample
        """
        if gps.status != 'running':
            return errors['invalid_gps']
        #print 'deleting the animal %s ' % curAnimalRead
        errorMessage = '-1There was an error while deleting the animal record. Please try again. If the problem persists, try restarting simple sampler'
        #lets start by deleting the samples, but first log this events
        
        #log the gps data that we are going to link to this animal read
        gpsId = self.db.logGpsData(gps.data)
        try:
            self.db.curQuery = 'select id, barcode from samples where animalId = (select animalId from animal_reads where id=%s)' % curAnimalRead
            #print self.db.curQuery
            samples = self.db.dictQuery()
            for sample in samples:
                #for each of this sample, add a sample_read record and then delete them
                try:
                    self.db.logSampleRead(sample['barcode'], gpsId, 'deleted')
                except:
                    return errorMessage
                #deleting
                try:
                    self.db._query('delete from samples where id = %s' % sample['id'])
                except:
                    return errorMessage
        except:
            #print 'There was an error while deleting an animal and its samples'
            return errorMessage

        #log this event
        curAnimalRead = self.db.logAnimalRead(gpsId, curAnimalRead, 'deleting')
        
        #all is alright, now lets return the home page
        return """
            <div><h2>DGEA Sampling</h2><a href='javascript:DGEA.refreshPage()'><img class='refresh' src='resource?images/refresh.png' alt='Refresh' /></a><hr /></div>
            <form method='post' enctype='multipart/form-data' name='sampling'>
                <input type='hidden' name='page' value='simple'>
                <div class='scroller input' id='input_form'>%s</div>
            </form>
            <script type='text/javascript'>
                $('#info').html('');
                $('#general').html('');
                $('#error').html('');
            </script>
            """ % self.dgeaHome(gps)


    def showSites(self, postvars, gps):
        """
        Depending on the passed variables, either show all the sites or only show households within a certain radius
        """
        #print postvars
        if('show_all' in postvars):     #we want all sites
            return self.dgeaHome(gps, 1)
        else:
            radius = int(postvars['radius'][0]) if ('radius' in postvars) else self.radius
            return self.dgeaHome(gps, 0, 0, radius)


    def refreshSampler(self, postvars, gps):
        """
        Being tested and resolved on a case on case basis
        """
        if gps.status != 'running':
            return errors['invalid_gps']
        errorMessage = '-1Error! This test case is not handled. Please note it and inform the system developer! To continue using the sampler press F5.'
        #refreshing the page when the household is selected, and we want all the cattle from this household
        #the order of the cascading ifs is very important...take note!!
        #print postvars
        if('household' in postvars and 'cow2sample' in postvars):   #we are dealing with the radius feature on
            householdId = int(postvars['household'][0])
            cow2sample = int(postvars['cow2sample'][0])
            if(householdId != 0 and cow2sample == 0):
                #print 'get the cattle in the selected household'
                return self.householdCattle(householdId, gps)
            else:
                return errorMessage
        elif('household' in postvars and 'cow2sample' in postvars and 'sites' in postvars):   #we are dealing with all the sites and the households
            householdId = int(postvars['household'][0])
            cow2sample = int(postvars['cow2sample'][0])
            site = int(postvars['sites'][0])
            if(site != 0 and householdId == 0 and cow2sample == 0):    #we want all the household from this particular site
                #print 'get all the household in the selected site(%s)' % site
                return siteHouseholds(site, gps)
        elif('curAnimal' in postvars and 'comments' in postvars and 'sample' in postvars and 'curAnimalRead' in postvars):
            curAnimal = int(postvars['curAnimal'][0])
            sample = int(postvars['sample'][0])
            curAnimalReadId = int(postvars['curAnimalRead'][0])
            if(curAnimal != '' and curAnimalReadId != '' and sample == ''):     #the user is trying to refresh the page after a sample has been scanned and it was saved.
                return '-1The sampler cannot save the sample that was just scanned. Please scan the sample again for it to be saved.'
            else:
                return errorMessage
        elif('household' in postvars and 'radius' in postvars):
            #we need to update the radius of the households
            if(postvars['household'][0] != 0 and postvars['household'][0] != 0):
                #print 'refresh the cattle in the selected household'
                return self.householdCattle(int(postvars['household'][0]), gps)
        elif('household' in postvars):      #this test case should be last as its the most minimialistic
            householdId = int(postvars['household'][0])
            #if(household == 0):
                #print "dealing wit 'radiat'd' sites: refresh the households"
                
        else:
            return errorMessage


    def updateSites(self, postvars, gps):
        """
        The radius of interest has changed and there is need to get the households within this radius
        """
        if gps.status != 'running':
            return errors['invalid_gps']
        
        radius = int(postvars['radius'][0]) if ('radius' in postvars) else self.radius
        householdId = int(postvars['household'][0]) if('household' in postvars) else 0
        return self.householdsWithinRadius(gps, householdId, radius)
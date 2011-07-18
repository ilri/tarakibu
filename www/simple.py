import json
from common import *
from time import time

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


    def update(self, info):
        if info['active_tag']:
            if self.info_time + info['tag_read'] > time():
                output += ajax('info', self.db.sample_info(info['tag'])) 
            else:
                output += ajax('info',self.db.sample_info(info['active_tag']))
        else:
            output += ajax('info', info['msg'])
        output += ajax('error', info['error'])
        return output


    def new_animal(self, info):
        info['mode']       = 'animal'
        info['active_tag'] = None
        info['error']      = ''
        return self.input_form(info)


    def input_form(self, info):
        output = ''
        print info
        if info['mode'] == 'animal':
            if info['target'] == 'dgea':
                return self.dgeaHome()


    def dgea_form(self, info):
        info['target'] = 'random'
        return self.input_form(info)


    def site(self, info):
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
                          <h1>%s</h1>
                      </div>
                      <div class='box main' id='main_box'>
                        <h2><a href='javascript:;'>DGEA Sampling</a></h2>
                        <hr />
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
                  <a href='/admin'>< Administration page</a> * %s v. %s. &copy; Martin Norling, AVID Project, ILRI, 2010 * <a href='/site'>Site information >></a>
              </div>
            </div>
              <script type='text/javascript'>
                  $('#dgea_sampling').bind('click', DGEA.ajaxFunction);
                  $('[name=submit]').bind('click', {module: 'simple/dgea_form'}, DGEA.submitForm);
              </script>
            </body>
          </html>
          """ % (self.title, self.version, self.port, self.title, self.dgeaHome(), self.title, self.version)


    def dgeaHome(self):
        """
        Creates the home page of the DGEA sampler
        """
        return """
            <table>
            <tr><th colspan=2>Select the cow being sampled</td></tr>
            <tr><td>Sites:</td><td><select name='sites'>%s</select></td></tr>
            <tr><td>Household ID:</td><td><select name='household' onChange='javascript:DGEA.fetchHouseholdCattle();'><option value='0'>Select a Household</option>%s</select></td></tr>
            <tr><td>Cattle ID:</td><td id='householdCattle'><select><option value='0'>Select One</option></select></td></tr>
            </table>
            <script type='text/javascript'>
                $('[name=household]').bind('change', DGEA.fetchHouseholdCattle);    //seems this javascript scripts are not being implemented...quite sad
            </script>
            """ % (self.allSites(), self.allHouseholds())


    def get_animal_id(self, location, species = 'sheep', wrap = True):
        if wrap:
            return ajax_value('animal_id', self.db.get_next_animal_id(location, species))
        return self.db.get_next_animal_id(location, species)


    def cattleInSite(self):
        """
        Create a select component for the cattle
        """
        output = ''
        for animal in self.db.getCattle():
            output += "<option value='%s'>%s</option>" % (animal[0], animal[0])
        return output


    def allHouseholds(self):
        """
        Create a select component for the household
        """
        output = ''
        for household in self.db.getHouseholds():
            output += '<option value=\'%s\'>%s</option>' % (household[1], household[0])
        return output


    def allSites(self):
        """
        Create a select component for the sites
        """
        output = "<option value='0'>Select One"
        for site in self.db.getSites():
            output += '<option value=\'%s\'>%s</option>' % (site[0], site[0])
        return output


    def animal_input(self):
        return """Animal tag: <input type='text' name='animal' id='animal'>"""


    def parse_form(self, form, info, devices):
        print 'him!'
        if 'household' in form:
            """
            A household has been selected, get all the animals in this household
            """
            if devices['gps'].status == 'running':
                self.selectedHousehold(form, info, devices)
            else:
                print errors['invalid_gps']
                
        if 'household' in form or 'species' in form:
            if devices['gps'].status == 'running':
                try:
                    if 'species' in form:
                        self.input_random(form, info, devices)
                    else:
                        self.input_animal(form, info, devices)
                except:
                    info['error'] = errors['unknown_tag']
            else:
                info['error'] = errors['animal_no_gps']
        elif 'village' in form:
            self.input_location(form, info, devices)
        else:
            self.input_sample(form, info, devices)


    def input_animal(self, form, info, devices):
        if self.db.verify_tag(form['animal'][0]):
            self.db.insert_tag_read(form['animal'][0], devices['gps'].data)
            info['mode'] = 'sample'
            info['msg'] = 'Input samples using the barcode reader or keyboard.'
            info['active_tag'] = form['animal'][0]
            info['error'] = ''
        else:
            raise 


    def input_sample(self, form, info, devices):
        if devices['gps'].status == 'running':
            if self.db.verify_sample(form['sample'][0]):
                self.db.insert_sample(form['sample'][0], info['active_tag'], devices['gps'].data, form['comment'][0])
                previous = '%s' % self.db.get_samples(info['active_tag'])
                info['error'] = ''
            else:
                info['error'] = errors['invalid_barcode']
        else:
            info['error'] = errors['sample_no_gps']


    def input_random(self, form, info, devices):
        self.db.insert_tag_read(form['animal_id'][0], devices['gps'].data)
        if self.db.input_random_animal(form):
            info['mode'] = 'sample'
            info['msg'] = 'Input samples using the barcode reader or keyboard.'
            info['active_tag'] = form['animal_id'][0]
            info['error'] = ''
        else:
            raise Exception('Could not insert animal into database')


    def input_location(self, form, info, devices):
        village_info = self.db.get_village_info(form['village'][0]);
        if not village_info:
            info['error'] = 'Village %s not found in the database!' % form['village'][0]
        else:
            info['error'] = ''
            info['farmer'] = form['farmer'][0]
            self.db.insert_place(form['village'][0], devices['gps'].data['latitude'],
                                 devices['gps'].data['longtitude'], 0.5)


    def selectedHousehold(self, householdId, devices):
        print 'we here'
        if devices['gps'].status == 'running':
            return self.householdCattle(householdId, devices)
        else:
            print errors['invalid_gps']
            return "<span class='invalid_gps'>%s</span>" % errors['invalid_gps']


    def householdCattle(self, householdId, devices):
        """
        Do the necessary checks for this household and then select all the cattle from this household
        """
        #check that the current location of this household falls within the radius of where we expect it to be
        
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


    def collectSample(self, postvars, devices):
        """
        We are now ready to start the sample collection. We have the household where we sampling and the animal that we want sampled.
        
        Logging this event to the database and then we create the form that will be used to collect the data
        """
        print 'sampling a cow'
        if devices['gps'].status != 'running':
            return 'Invalid GPS data, cannot continue!'
        #log the gps data that we are going to link to this animal read
        gpsId = self.db.logGpsData(devices['gps'].data)
        #add the animal read instance to the database
        try:
            curAnimalRead = self.db.logAnimalRead(gpsId, postvars['cow2sample'][0], 'adding')
        except:
            print 'Serious error while adding the animal read to the database.'
            return """
                <h2><a href='javascript:;'>DGEA Sampling</a></h2>
                <hr />
                <form method='post' enctype='multipart/form-data' name='sampling'>
                    <input type='hidden' name='page' value='simple'>
                    <div class='scroller input' id='input_form'>%s</div>
                </form>
                <script>
                    $('#error').html('There was an error while adding data to the database. Please try again and if the problem persists, please restart simple sampler.');
                    setTimeout('DGEA.clearInformation()', 5000);
                </script>
            """ % self.dgeaHome()
        
        #now get the details of the animal that we are sampling
        query = 'select a.name as animalName, b.hhid, c.name as siteName from dgea_animals as a inner join households as b on a.hhId = b.id inner join sites as c on b.siteId = c.id where a.id=%s' % postvars['cow2sample'][0]
        res = self.db._query(query)
        res = res[0]
        curAnimal = res[2] + ', ' + res[1] + ', ' + res[0]
        return self.samplingPage(curAnimal, curAnimalRead, postvars['cow2sample'][0])


    def samplingPage(self, curAnimal, curAnimalRead, curAnimalId):
        """
        Creates the page to allow the user to start scanning the samples
        """
        print 'current animal - %s' % curAnimal
        print 'current animal read - %s' % curAnimalRead
        #get all the samples associated with this animal
        allSamples = self.animalSamples(curAnimalId)
        if isinstance(allSamples, str):
            return '-1%s' % allSamples
        print allSamples
        return """
            <h2><a href='javascript:;'>DGEA Sampling</a></h2>
            <hr />
            <form method='post' enctype='multipart/form-data' name='sampling'>
                <input type='hidden' name='page' value='simple'>
                Current Animal: <b>%s</b>&nbsp;<image src='resource?images/delete.png' alt='close' class='delete_animal %s' />
                <hr />
                <table>
                <tr> <td>Sample tube:</td> <td><input type='text' name='sample' id='sample'>  </td> </tr>
                <tr> <td>Information:</td> <td><input type='text' name='comments' id='comments'></td> </tr>
                <input type='hidden' name='curAnimalRead' value='%s' />
                <input type='hidden' name='curAnimal' value='%s' />
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
            """ %  (curAnimal, curAnimal, curAnimalRead, curAnimal, json.dumps({'animal': curAnimal, 'samples': allSamples}))


    def saveSample(self, postvars, devices, barcodedSamples):
        """
        We are adding a sample to a cow which was selected before
        
        @todo sanitize the comments
        @todo change the status of a sample read to re-sampled if the user specified a sample which is already in the database
        """
        errorMessage = {'error': 'There was an error while adding the sample to the database. Please try again. If the problem persists, please restart the simple sampler.'}
        barcode = postvars['barcode'][0].upper()
        curAnimal = postvars['curAnimal'][0]
        #check if this sample has been added before
        res = self.isSampleSaved(barcode)
        print res
        if isinstance(res, str):    #an error occured while checking whether the sample has been saved before
            return res
        elif isinstance(res, dict):    #we have an array, meaning that the sample has bee saved before
            print 'saved already'
            return json.dumps(res)
            
        if devices['gps'].status != 'running':
            return json.dumps({'error': "The current GPS coordinates are not valid. Please wait until you get a valid GPS coordinate and then try again."});
        
        #lets save this sample, but first get the animalId
        try:
            query = 'select animalId from animal_reads where id=%s' % postvars['curAnimalRead'][0]
            res = self.db._query(query)
        except:
            return errorMessage
        
        curAnimalId = res[0][0]
        #Lets do the necessary data checks
        if (barcodedSamples == 'yes'): #we have barcoded samples, so check whether we have a good barcode as per the defined barcodes in the database
            if (self.db.isBarcodePrefixDefined(barcode) == 1):
                return 'Invalid barcode prefix'
            barcodeRe = re.compile('[^0-9]{5,6}$')
            if barcodeRe.match(barcode):
                return 'Invalid sample barcode!'
        #log this sample read
        try:
            self.db.logSampleRead(barcode, self.gps.data, 'added')
        except:
            return errorMessage

        #we are now all set...so lets proceed to the db stuff
        try:
            query = "insert into samples(barcode, animalReadId, animalId, comment) values('%s', '%s', '%s', '%s')" % (barcode, postvars['curAnimalRead'][0], curAnimalId, postvars['comments'][0],)
            self.db._query(query)
        except:
            return errorMessage
        #we are ok, return all the samples from this animal
        self.db.curQuery = 'select b.* from animal_reads as a inner join samples as b on a.animalId=b.animalId where a.id=%s' % postvars['curAnimalRead'][0]
        try:
            samples = self.db.dictQuery()
            allSamples = []
            for sample in samples:
                allSamples.append({'barcode': sample['barcode'], 'sampling_date_time': str(sample['sampling_date_time'])})
            print allSamples
        except:
            print 'There was an error while fetching samples'
            return errorMessage
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
            print "Error while checking if a sample exists. " + self.db.curQuery
            return errorMessage
        
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


    def nextAnimal(self, postvars, devices):
        """
        We have finalized sampling one animal, now we need to save the current samples and move to the next animal
        """
        print 'here we are'
        if devices['gps'].status != 'running':
            return errors['invalid_gps']
        #All the samples have been already saved...jst show the home page again
        return """
            <h2><a href='javascript:;'>DGEA Sampling</a></h2>
            <hr />
            <form method='post' enctype='multipart/form-data' name='sampling'>
                <input type='hidden' name='page' value='simple'>
                <div class='scroller input' id='input_form'>%s</div>
            </form>
            <script type='text/javascript'>
                DGEA.curAnimal = {};
                alert('refreshing the page');
                DGEA.clearInformation();
            </script>
        """ % self.dgeaHome()


    def animalSamples(self, animalId):
        """
        Gets all the samples that have been saved from this animal
        """
        errorMessage = 'There was an error while fetching animal samples data from the database. Please try again. If the problem persists, please restart the simple sampler.'
        self.db.curQuery = "select sampling_date_time, barcode from samples where animalId = %s" % animalId
        try:
            samples = self.db.dictQuery()
            allSamples = []
            for sample in samples:
                allSamples.append({'barcode': sample['barcode'], 'sampling_date_time': str(sample['sampling_date_time'])})
        except:
            print "Error while fetching samples associated with a certain animal. " + self.db.curQuery
            return errorMessage
        #we all good, return the samples
        return allSamples


    def animalDisplayName(self, animalId):
        """
        Get the full name of this animal. By the full name we mean the name of the animal that we are going to display
        """
        self.db.curQuery = 'select a.name as animalName, b.hhid, c.name as siteName from dgea_animals as a inner join households as b on a.hhId = b.id inner join sites as c on b.siteId = c.id where a.id=%s' % animalId
        try:
            animal = self.db.dictQuery()
            animalDetails = animal[0]['siteName'] + ', ' + animal[0]['hhid'] + ', ' + animal[0]['animalName']
        except:
            print "Error while fetching the animal full name" + self.db.curQuery
            return errorMessage
        return {'animalName': animalDetails}


    def deleteSample(self, sample, devices):
        """
        The user wants this sample deleted. We are going to delete it from the samples records, but add this entry into the sample reads table
        
        Returns a json object with the current animal information in case all went successfully, else it returns a json with the error
        """
        errorMessage = {'error': 'There was an error while deleting the sample from the database. Please try again. If the problem persists, please restart the simple sampler.'}
        if devices['gps'].status != 'running':
            return json.dumps({'error': errors['invalid_gps']})
        #jst for the sakes of it, lets ensure that the sample is actually sampled
        res = self.isSampleSaved(sample)
        if res == 0:
            mssg = "Error, Trying to delete '%s'. We actually do not have this sample." % sample
            return json.dumps({'error': mssg})
        #we actually have the sample, so lets delete it
        #log this sample delete
        try:
            self.db.logSampleRead(sample, self.gps.data, 'deleted')
        except:
            return json.dumps(errorMessage)
        #the actual delete
        query = "delete from samples where barcode = '%s'" % sample
        self.db._query(query)
        msg = "The sample '%s' has been deleted succesfully!" % sample
        
        #now get the other samples for this animal
        allSamples = self.animalSamples(res['animalId'])
        print allSamples
        if isinstance(allSamples, str):
            return json.dumps({'error': allSamples})
            
        #get the animal display name
        animalDetails = self.animalDisplayName(res['animalId'])
        if isinstance(animalDetails, str):
            return animalDetails
        animalName = animalDetails['animalName']
        return json.dumps({'animal': animalName, 'samples': allSamples, 'mssg': msg})


    def deleteAnimal(self, curAnimalRead, devices):
        """
        Deletes a sampled animal and also deletes all the samples associated with the current sample
        """
        if devices['gps'].status != 'running':
            return errors['invalid_gps']
        print 'deleting the animal %s ' % curAnimalRead
        errorMessage = '-1There was an error while deleting the animal record. Please try again. If the problem persists, try restarting simple sampler'
        #lets start by deleting the samples, but first log this events
        try:
            self.db.curQuery = 'select id, barcode from samples where animalId = (select animalId from animal_reads where id=%s)' % curAnimalRead
            samples = self.db.dictQuery()
            for sample in samples:
                #for each of this sample, add a sample_read record and then delete them
                try:
                    self.db.logSampleRead(sample['barcode'], self.gps.data, 'deleted')
                except:
                    return errorMessage
                #deleting
                try:
                    self.db._query('delete from samples where id = %s' % sample['id'])
                except:
                    return errorMessage
        except:
            print 'There was an error while deleting an animal and its samples'
            return errorMessage

        #log this event
        curAnimalRead = self.db.logAnimalRead(gpsId, postvars['cow2sample'][0], 'deleting')
        
        #all is alright, now lets return the home page
        return """
            <h2><a href='javascript:;'>DGEA Sampling</a></h2>
            <hr />
            <form method='post' enctype='multipart/form-data' name='sampling'>
                <input type='hidden' name='page' value='simple'>
                <div class='scroller input' id='input_form'>%s</div>
            </form>
            """ % self.dgeaHome()
    
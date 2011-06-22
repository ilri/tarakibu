from common import *
from time import time

errors = {'label':'Could not verify tag label. Verify that this animal is part of the sampling process and try again',
          'unknown_tag':'The tag you have input is not featured in the animal database. This animal is not part of the sampling program.',
          'invalid_barcode':'Already scanned or not a valid barcode',
          'animal_no_gps':'Cannot input tag read without gps position.',
          'sample_no_gps':'Cannot input sample without gps position.'}

class simple(SimplePage):

    def update(self, info):
        output = SimplePage.update(self, info)
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
        if info['mode'] == 'animal':
            if info['target'] == 'livestock':
                output += ajax('input_form', self.animal_input())
                output += self.focus('animal')
            else:
                output += ajax('input_form', self.random_input(info['farmer']))     #just update the page
        else:
            output += ajax('input_form', self.sample_input(info['active_tag'], self.port))
            output += self.focus('sample')
        return output

    def livestock_form(self, info):
        info['target'] = 'livestock'
        return self.input_form(info)

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
            DGEA.updateSite('simple');
            DGEA.ajaxFunction('simple/input_form');   //this needs to be called only once when the page finishes loading not recursively
        });
    </script>
  </head>
  <body>
    <div class='site'>
        <div class='left'>
            <div class='box top'>
                <h1>%s</h1>
            </div>
            <div class='box main'>
                <h2><a id='dgea_sampling' href="javascript:DGEA.ajaxFunction('simple/dgea_form')";>DGEA Sampling</a></h2>
                <hr />
                <form action='?' method='post' name='sampling'>
                    <input type='hidden' name='page' value='simple'>
                    <div class='scroller input' id='input_form'></div>
                    <hr />
                    <div class='submitbutton'><input type='submit' value='Submit'></div>
                </form>
            </div>
        </div>
        <div class='right'>
            <div class='box top'>
                <table>
                    <tr><td>GPS:</td><td><div id='position'></div></td></tr>
                </table>
            </div>
        <div class='box main'>
            <h2>Information</h2>
            <hr />
            <div class='scroller info' id='info'></div>
            <div class='scroller error' id='error'></div>
        </div>
    </div>
    <div class='footer'>
        <a href='/admin'>< Administration page</a> * %s v. %s. &copy; Martin Norling, AVID Project, ILRI, 2010 * <a href='/site'>Site information >></a>
    </div>
  </div>
    <script type='text/javascript'>
        $('#dgea_sampling').bind('click', DGEA.ajaxFunction);
    </script>
  </body>
</html>
""" % (self.title, self.version, self.port, self.title, self.title, self.version)

    def focus(self, target):
        return 'document.sampling.%s.focus();' % target

    def random_input(self, farmer = ''):
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
        output = ''
        for site in self.db.getSites():
            output += '<option value=\'%s\'>%s</option>' % (site[0], site[0])
        return output
        
    def selectedSite(self, info):
        """
        create a select component for the households in the selected sites
        """

    def animal_input(self):
        return """Animal tag: <input type='text' name='animal' id='animal'>"""

    def sample_input(self, title, port):
        return """
Current Animal: %s
<hr />
<table>
<tr> <td>Sample tube:</td> <td><input type='text' name='sample' id='sample'>  </td> </tr>
<tr> <td>Information:</td> <td><input type='text' name='comment' id='comment'></td> </tr>
</table>
<hr />
<a href=javascript:ajaxFunction('http://localhost:%s/','simple/new_animal')>Next Animal</a> >>
""" % (title.upper(), port) 

    def parse_form(self, form, info, devices):
        print form
        if 'household' in form:
            """
            A household has been selected, get all the animals in this household
            """
            if devices['gps'].status == 'running':
                self.selectedHousehold(form, info, devices)
            else:
                print "No valid GPS coordinates...cannot proceed!";
                
        elif 'household' in form and 'cattleId' in form:
            """
            Ready to start adding the samples to this particular animal
            """
            
            
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
        if devices['gps'].status == 'running':
            return self.householdCattle(householdId, devices)
        else:
            print "No valid GPS coordinates...cannot proceed!";
            
        
    def householdCattle(self, householdId, devices):
        """
        Do the necessary checks for this household and then select all the cattle from this household
        """
        #check that the current location of this household falls within the radius of where we expect it to be
        
        #seems all is ok, get all the animals associated with this household
        cattleInHousehold = self.db.getHouseholdCattle(householdId)
        #now lets create the dropdown for the animals
        output = "<select name='cow2sample'>"
        for cow in cattleInHousehold:
            output += '<option value=\'%s\'>%s</option>' % (cow[0], cow[1])
        output += '</select>'
        return output

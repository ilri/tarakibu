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
        if self.devices['rfid'].data and info['mode'] == 'animal':
            try:
                info['active_tag'] = self.db.tag_to_label(\
                                                 self.devices['rfid'].data)[0]
                if info['active_tag']:
                    self.db.insert_tag_read(info['active_tag'],
                                            self.devices['gps'].data)
                    info['mode'] = 'sample'
                    self.devices['rfid'].data = None
                    output += ajax('input_form',
                              self.sample_input(info['active_tag'], self.port))
                    output += self.focus('sample')
            except:
                info['error'] = errors['label']
        if self.devices['rfid'].data and info['mode'] == 'sample':
            try:
                info['tag']=self.db.tag_to_label(self.devices['rfid'].data)[0]
                info['tag_read'] = time()
                self.devices['rfid'].data = None
            except:
                pass
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
                output += ajax('input_form', self.random_input(info['farmer']))
                output += self.focus('species')
        else:
            output += ajax('input_form', self.sample_input(info['active_tag'],
                                                           self.port))
            output += self.focus('sample')
        return output

    def livestock_form(self, info):
        info['target'] = 'livestock'
        return self.input_form(info)

    def random_form(self, info):
        info['target'] = 'random'
        return self.input_form(info)

    def site(self, info):
        return """<html>
  <head>
    <title>%s v. %s</title>
    <script type=\'text/javascript\'>
    %s
      function updateSite()
      {
        ajaxFunction('http://localhost:%s/','simple/update')
        setTimeout('updateSite()', 500)
      }
      function updateAnimalID(value)
      {
        var element = document.getElementById('animal_id')
        var part = element.value.split("/")
        ajaxFunction('http://localhost:8080/','simple/get_animal_id/' + part[0] + '/' + value );
      }
    </script>
    %s
  </head>
  <body onLoad="updateSite(); ajaxFunction('http://localhost:%s/','simple/input_form')">
    <div class='site'>
      <div class='left'>
        <div class='box top'>
          <h1>%s</h1>
        </div>
        <div class='box main'>
          <h2><a href=javascript:ajaxFunction('http://localhost:%s','/simple/livestock_form')>Livestock</a>|
              <a href=javascript:ajaxFunction('http://localhost:%s','/simple/random_form')>Random</a></h2>
          <hr />
          <form action='http://localhost:%s/' method='post' enctype='multipart/form-data' name='sampling'>
            <input type='hidden' name='page' value='simple'>
            <div class='scroller input' id='input_form'></div>
            <hr />
            <div class='submitbutton'>
              <input type='submit' value='Submit'>
            </div>
          </form>
        </div>
      </div>
      <div class='right'>
        <div class='box top'>
          <table>
            <tr><td>GPS:</td><td><div id='position'></div></td></tr>
            <tr><td>RFID:</td><td><div id='reader'></div></td></tr>
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
        <a href='/admin'><< Administration page</a> * %s v. %s. &copy; Martin Norling, AVID Project, ILRI, 2010 * <a href='/site'>Site information >></a>
      </div>
    </div>
  </body>
</html>
""" % (self.title, self.version, ajax_function(self.port), self.port, \
       site_style(), self.port, self.title, self.port, self.port, self.port, self.title, self.version)

    def focus(self, target):
        return 'document.sampling.%s.focus();' % target

    def random_input(self, farmer = ''):
        if not self.db.get_location(self.gps):
            return """
<table>
<tr><th colspan=2>Enter new location</td></tr>
<tr><td>Village:</td><td><input type='text' name='village' value=''></td></tr>
<tr><td>Farmer:</td><td><input type='text' name='farmer' value=''></td></tr>
</table>
"""
        return """
<table>
<tr><td>Species:</td><td><select name='species' onChange='updateAnimalID(this.value)'>%s</select></td></tr>
<tr><td>Animal ID:</td><td><input type='text' id='animal_id' name='animal_id' value='%s'></td></tr>
<tr><td>Approximate Age:</td><td><select name='age'><option name='<1'>&lt;1</option><option name='1-2'>1-2</option><option name='>2'>&gt;2</option></select></td></tr>
<tr><td>Sex</td><td><select name='sex'><option name='female'>female</option><option name='male'>male</option><option name='castrated'>castrated</option></select></td></tr>
<tr><td>Last RVF Vaccine:</td><td><input type='text' name='rvf'></td></tr>
<tr><td>Other Vaccines:</td><td><input type='text' name='rvf'></td></tr>
<tr><td>Comment:</td><td><input type='text' name='comment'></td></tr>
</table>
<input type='hidden' name='owner' value='%s'>
<input type='hidden' name='location' value='%s'>
""" % (self.get_species(), self.get_animal_id(self.db.get_location(self.gps), 'sheep', False), farmer, self.db.get_location(self.gps))
    
    def get_animal_id(self, location, species = 'sheep', wrap = True):
        if wrap:
            return ajax_value('animal_id', self.db.get_next_animal_id(location, species))
        return self.db.get_next_animal_id(location, species)

    def get_species(self):
        output = ''
        for animal in self.db.get_species():
            output += '<option value=\'%s\'>%s</option>' % (animal[0], animal[0])
        return output

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
        if 'animal' in form or 'species' in form:
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
                self.db.insert_sample(form['sample'][0], info['active_tag'], \
                                      devices['gps'].data, form['comment'][0])
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

        

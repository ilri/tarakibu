from common import *
from time import time

errors = {'label':'Could not verify tag label. Verify that this animal is part of the sampling process and try again',\
          'unknown_tag':'The tag you have input is not featured in the animal database. This animal is not part of the sampling program.',\
          'invalid_barcode':'Already scanned or not a valid barcode',\
          'animal_no_gps':'Cannot input animal without gps position.',\
          'sample_no_gps':'Cannot input sample without gps position.'}

class simple():
    def __init__(self, settings, db):
        self.title = settings['name']
        self.version = settings['version']
        self.port = settings['port']
        self.info_time = settings['info_time']
        self.db = db

    def update(self, devices, info):
        output = ''
        output += ajax('position', position(devices['gps']))
        output += ajax('reader',   reader(devices['rfid']))
        if info['active_tag']:
            if self.info_time + info['tag_read'] > time():
                output += ajax('info', self.db.sample_info(info['tag'])) 
            else:
                output += ajax('info', self.db.sample_info(info['active_tag']))
        else:
            output += ajax('info', info['msg'])
        output += ajax('error', info['error'])
        if devices['rfid'].data and info['mode'] == 'animal':
            try:
                info['active_tag'] = self.db.tag_to_label(\
                                                    devices['rfid'].data)[0]
                if info['active_tag']:
                    self.db.insert_tag_read(info['active_tag'],\
                                            devices['gps'].data)
                    info['mode'] = 'sample'
                    devices['rfid'].data = None
                    output += ajax('input_form',\
                              self.sample_input(info['active_tag'], self.port))
                    output += self.focus('sample')
            except:
                info['error'] = errors['label']
        if devices['rfid'].data and info['mode'] == 'sample':
            try:
                info['tag'] = self.db.tag_to_label(devices['rfid'].data)[0]
                info['tag_read'] = time()
                devices['rfid'].data = None
            except:
                pass
        return output

    def new_animal(self, info):
        info['mode'] = 'animal'
        info['active_tag'] = None
        output = ''
        output += ajax('input_form', self.animal_input())
        output += self.focus('animal')
        info['error'] = ''
        return output

    def input_form(self, info, settings):
        output = ''
        if info['mode'] == 'animal':
            output += ajax('input_form', self.animal_input())
            output += self.focus('animal')
        else:
            output += ajax('input_form', self.sample_input(info['active_tag'],\
                                                           settings['port']))
        output += self.focus('sample')
        return output

    def site(self):
        return """<html>
  <head>
    <title>%s v. %s</title>
    <script type=\'text/javascript\'>
    %s
      function updateSite()
      {
        ajaxFunction('http://localhost:%s/','update')
        setTimeout('updateSite()', 500)
      }
    </script>
    %s
  </head>
  <body onLoad="updateSite(); ajaxFunction('http://localhost:%s/','input_form')">
    <div class='site'>
      <div class='left'>
        <div class='box top'>
          <h1>%s</h1>
        </div>
        <div class='box main'>
          <h2>Sample Input</h2>
          <hr />
          <form action='http://localhost:%s/' method='post' enctype='multipart/form-data' name='sampling'>
            <input type='hidden' name='page' value='default'>
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
            <tr><td>Position:</td><td><div id='position'></div></td></tr>
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
       site_style(), self.port, self.title, self.port, self.title, self.version)

    def focus(self, target):
        return 'document.sampling.%s.focus();' % target

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
<a href=javascript:ajaxFunction('http://localhost:%s/','new_animal')>Next Animal</a> >>
""" % (title.upper(), port) 

    def parse_form(self, form, info, devices):
        if 'animal' in form:
            if devices['gps'].status == 'running':
                try:
                    self.input_animal(form, info, devices)
                except:
                    info['error'] = errors['unknown_tag']
            else:
                info['error'] = errors['animal_no_gps']
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
                self.db.insert_sample(form['sample'][0],   info['active_tag'], \
                                      devices['gps'].data, form['comment'][0])
                previous = '%s' % self.db.get_samples(info['active_tag'])
                info['error'] = ''
            else:
                info['error'] = errors['invalid_barcode']
        else:
            info['error'] = errors['no_gps']
    

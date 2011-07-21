"""
 Copyright 2011 ILRI
 
 This file is part of <ex simple sampler>.
 
 <ex simple sampler> is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 <ex simple sampler> is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with <ex simple sampler>.  If not, see <http://www.gnu.org/licenses/>.
 
"""

from common import *

class admin(SimplePage):

    def site(self, info):
        """
        Creates the admin's home page
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
                          <h1><a href='http://localhost:%s/admin'>%s</a></h1>
                      </div>
                      <div class='box main' id='main_box'>
                        <h2>Admin Page</h2>
                        <hr />
                        <form method='post' enctype='multipart/form-data' name='sampling'>
                          <input type='hidden' name='page' value='simple'>
                          <div class='scroller input' id='input_form'>I dunno what to include in this page...so I am waiting for ideas</div>
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
                      <h2>Extra Information</h2>
                      <hr />
                      <div class='scroller info' id='info'></div>
                      <div class='scroller general' id='general'></div>
                      <div class='scroller error' id='error'></div>
                  </div>
              </div>
              <div class='footer'>
                  <a href='/'>< Sampling Page</a> * %s v. %s. &copy; AVID Team, AVID Project, ILRI, 2010 * <a href='/summary'>Sampling Summary >></a>
              </div>
            </div>
              <script type='text/javascript'>
                  $('[name=submit]').bind('click', {module: 'simple/dgea_form'}, DGEA.submitForm);
              </script>
            </body>
          </html>
          """ % (self.title, self.version, self.port, self.port, self.title, self.title, self.version)


    def sample_types(self, info):
        info  = '<table>'
        info += '<tr><th>Prefix</td><th>Sample Type</td></tr>'
        for t in self.db.get_sample_types():
            info += '<tr><td>%s</td><td>%s</td></tr>' % t
        info += '</table>'
        form  = 'Add Sample Type:'
        form += '<table>'
        form += '<tr><th>Prefix</td><td><input type=\'text\' name=\'prefix\'></td></tr>'
        form += '<tr><th>Sample Type</td><td><input type=\'text\' name=\'description\'></td></tr>'
        form += '</table>'
        return ajax('info', info) + ajax('input_form', form)
    
    def places(self, info):
        info  = '<table>'
        info += '<tr><th>Name</td><th>Latitude</td><th>longitude</td><th>Radius</td></tr>'
        for p in self.db.get_places():
            info += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % p
        info += '</table>'
        lat = ''
        lon = ''
        if self.devices['gps'].status == 'running':
            lat = gps_format(self.devices['gps'].data['latitude'])
            lon = gps_format(self.devices['gps'].data['longitude'])
        form  = 'Add Place:'
        form += '<table>'
        form += '<tr><th>Name</td><td><input type=\'text\' name=\'name\'></td><td></td></tr>'
        form += '<tr><th>Latitude</td><td><input type=\'text\' name=\'latitude\' value=\'%s\'></td><td></td></tr>' % lat
        form += '<tr><th>longitude</td><td><input type=\'text\' name=\'longitude\' value=\'%s\'></td><td></td></tr>' % lon
        form += '<tr><th>Radius</td><td><input type=\'text\' name=\'radius\' value=\'1\'></td><td>km</td></tr>'
        form += '</table>'
        return ajax('info', info) + ajax('input_form', form)
    
    def tags(self, info):
        info  = '<table>'
        info += '<tr><th><small>Label</small></td><th><small>RFID</small></td><th><small>Color</small></td><th><small>Supplier</small></td><th></small>Type</td></tr>' 
        for tag in self.db.get_tags():
            info += '<tr><td><small>%s</small></td><td><small>%s</small></td><td><small>%s</small></td><td><small>%s</small></td><td><small>%s</small></td></tr>' % tag
        info += '</table>'
        form  = 'Replace tag:<select name=\'replace\'>'
        for tag in self.db.get_tags():
            form += '<option name=\'%s\'>%s</option>' % (tag[0], tag[0])
        form += '</select><br>'
        form += 'Replace with:'
        form += '<table>'
        form += '<tr><th>Label:</td><td><input type=\'text\' name=\'tag\'></td></tr>'
        form += '<tr><th>RFID:</td><td><input type=\'text\' name=\'rfid\'></td></tr>'
        form += '<tr><th>Color:</td><td><input type=\'text\' name=\'color\'></td></tr>'
        form += '<tr><th>Supplier:</td><td><input type=\'text\' name=\'supplier\'></td></tr>'
        form += '<tr><th>Type:</td><td><input type=\'text\' name=\'tag_type\'></td></tr>'
        form += '</table>'
        return ajax('info', info) + ajax('input_form', form)
    
    def animals(self, info):
        info  = '<table>'
        info += '<tr><th>Tag</td><th>Sex</td><th>Owner</td><th>Location</td></tr>'
        form  = 'Replace animal:<select name=\'replace\'>'
        for animal in self.db.get_animals():
            info += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % animal
            form += '<option name=\'%s\'>%s</option>' % (animal[0], animal[0])
        form += '</select><br>'
        form += 'Replace with:'
        form += '<table>'
        form += '<tr><td>New tag:</td><td><input type=\'text\' name=\'new_tag\'></td><td></td></tr>'
        form += '<tr><td>Date of Birth</td><td><input type=\'text\' name=\'date_of_birth\'></td><td>ex. 2010-01-01</td></tr>'
        form += '<tr><td>Gender</td><td><select name=\'sex\'><option name=\'female\'>female</option><option name=\'male\'>male</option></select></td><td></td></tr>'
        form += '<tr><td>Owner</td><td><input type=\'text\' name=\'owner\'></td><td></td></tr>'
        form += '<tr><td>Weight</td><td><input type=\'text\' name=\'weight\'></td><td></td></tr>'
        form += '<tr><td>Comment</td><td><input type=\'text\' name=\'comment\'></td><td></td></tr>'
        form += '</table>'
        info += '</table>'
        return ajax('info', info) + ajax('input_form', form)
    
    def parse_form(self, form, info, devices):
        if 'prefix' in form:
            self.db.insert_prefix(form['prefix'][0], form['description'][0])
        elif 'radius' in form:
            self.db.insert_place(form['name'][0], form['latitude'][0], \
                                 form['longitude'][0], form['radius'][0])
        elif 'rfid' in form:
            self.db.replace_tag(form['tag'][0], form['rfid'][0], \
                    form['color'][0], form['supplier'][0], form['tag_type'][0],\
                    form['replace'][0])
        elif 'sex' in form:
            self.db.replace_animal(form['replace'][0],
                                   form['new_tag'][0],
                                   form['date_of_birth'][0],
                                   form['sex'][0],
                                   form['owner'][0],
                                   form['weight'][0],
                                   form['comment'][0])
        return ''

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

"""
CHANGELOG
========================
	- Separated all the javascript and css from the HTML
"""

from common import *

class summary(SimplePage):

    def site(self, info):
        """
        Creates the summary home page
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
                        <h2>Summary Page</h2>
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
                  <a href='/'>< Sampling Page</a> * %s v. %s. &copy; AVID Team, AVID Project, ILRI, 2010 * <a href='/admin'>Administration Page >></a>
              </div>
            </div>
              <script type='text/javascript'>
                  $('[name=submit]').bind('click', {module: 'simple/dgea_form'}, DGEA.submitForm);
              </script>
            </body>
          </html>
          """ % (self.title, self.version, self.port, self.port, self.title, self.title, self.version)

    def parse_form(self, form, info, devices):
        samples = {}
        for label in form:
            if label != 'page':
                tag = label[:9]
                if tag not in samples.keys():
                    samples[tag] = ['',('delete', False)]
                if label[9:] == 'delete':
                    samples[tag][1] = ('delete', True)
                else:
                    samples[tag][0] = ('comment', form[label][0])
        for label in samples:
            self.db.update_samples(label, samples[label])
    
    def location(self, info):
        location = self.db.get_location(self.devices['gps'])
        info  = '<h3>Known animals at this Location</h3>'
        info += '<table>'
        info += '<tr><th>Tag</td><th>Sex</td><th>Owner</td><th>Location</td></tr>'
        for animal in self.db.get_animals_at_location(location):
            color = '#f00'
            if animal[4]:
                color = '#0f0'
            info += '<tr style=\'color:%s\'><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (color, animal[0], animal[1], animal[2], animal[3])
        info += '</table>'
        if location:
            output = ajax('where', 'You are at %s' % location)
            output += ajax('info', info)
        else:
            output = ajax('where', 'You are at an unknown position')
        return output
    
    def previous_samples(self, info):
        output  = '<table>'
        output += '<tr><th>Sample</td><th>Comment</td><th>Delete</td></tr>'
        for sample in self.db.get_latest_samples():
            output += '<tr><td>%s</td><td><input type=\'text\' name=\'%s\' value=\'%s\'></td><td><input type=\'checkbox\' name=\'%sdelete\'></td></tr>' % \
                (sample[0], sample[0], sample[2], sample[0])
        output += '</table>'
        return ajax('input_form', output)

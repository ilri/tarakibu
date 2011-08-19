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

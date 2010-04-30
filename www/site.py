from common import *

class site():
    def __init__(self, settings, db):
        self.title = settings['name']
        self.version = settings['version']
        self.port = settings['port']
        self.info_time = settings['info_time']
        self.db = db

    def site(self):
        return """<html>
  <head>
    <title>%s v. %s - Admin</title>
    <script type=\'text/javascript\'>
    %s
      function updateSite()
      {
        ajaxFunction('http://localhost:%s/','devices')
        setTimeout('updateSite()', 500)
      }
    </script>  
    %s
  </head>
  <body onLoad="updateSite();">
    <div class='site'>
      <div class='left'>
        <div class='box top'>
          <h1>Sampling Site</h1>
        </div>
        <div class='box main'>
          <h2>Latest Samples</h2>
          <hr />
          <form action='http://localhost:%s/' method='post' enctype='multipart/form-data' name='sampling'>
            <input type='hidden' name='page' value='admin'>
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
          <h2>Animals in this area</h2>
          <hr />
          <div class='scroller info large' id='info'></div>
        </div>
      </div>
      <div class='footer'>
        <a href='/'><< Sampling Page</a> * %s v. %s. &copy; Martin Norling, AVID Project, ILRI, 2010 * <a href='/admin'>Administration Page >></a>
      </div>
    </div>
  </body>
</html>
""" % (self.title, self.version, ajax_function(self.port), self.port, \
       site_style(), \
       self.port, self.title, self.version)
    
    def update(self, devices):
        output = ''
        output += ajax('position', position(devices['gps']))
        output += ajax('reader',   reader(devices['rfid']))
        return output
    

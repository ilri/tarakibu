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
        ajaxFunction('http://localhost:%s/','location')
        setTimeout('updateSite()', 500)
      }
    </script>  
    %s
  </head>
  <body onLoad="updateSite(); ajaxFunction('http://localhost:%s/','previous');">
    <div class='site'>
      <div class='left'>
        <div class='box top'>
          <h1>Sampling Site</h1>
        </div>
        <div class='box main'>
          <h2>Latest Samples</h2>
          <hr />
          <form action='http://localhost:%s/' method='post' enctype='multipart/form-data' name='sampling'>
            <input type='hidden' name='page' value='site'>
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
          <h2><div id='where'></div></h2>
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
       self.port, site_style(), self.port, \
       self.port, self.title, self.version)

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
    
    def location(self, gps):
        output = 'You are at an unknown position'
        for place in self.db.get_places():
            if gps.distance(place[1], place[2]) < place[3]:
                output = 'You are at %s' % place[0]
                break
        return ajax('where', output)
    
    def previous_samples(self):
        output  = '<table>'
        output += '<tr><th>Sample</td><th>Comment</td><th>Delete</td></tr>'
        for sample in self.db.get_latest_samples():
            output += '<tr><td>%s%s</td><td><input type=\'text\' name=\'%s%s\' value=\'%s\'></td><td><input type=\'checkbox\' name=\'%s%sdelete\'></td></tr>' % \
                (sample[0], sample[1], sample[0], sample[1], sample[3], sample[0], sample[1])
        output += '</table>'
        return ajax('input_form', output)

from common import *

class site(SimplePage):

    def site(self, info):
        return """
%s
      function updateSite()
      {
        ajaxFunction('http://localhost:%s/','site/update')
        ajaxFunction('http://localhost:%s/','site/location')
        setTimeout('updateSite()', 500)
      }
    </script>  
    %s
  </head>
  <body onLoad="updateSite(); ajaxFunction('http://localhost:%s/','site/previous_samples');">
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
            <tr><td>GPS:</td><td><div id='position'></div></td></tr>
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
""" % (self.header(), self.port, self.port, site_style(), self.port, \
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

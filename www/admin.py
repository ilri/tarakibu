from common import *

class admin():
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
  <body onLoad="updateSite(); ajaxFunction('http://localhost:%s/','types')">
    <div class='site'>
      <div class='left'>
        <div class='box top'>
          <h1>Administration</h1>
        </div>
        <div class='box main'>
          <h3><a href=javascript:ajaxFunction('http://localhost:%s','/types')>Sample Types</a> | 
              <a href=javascript:ajaxFunction('http://localhost:%s','/places')>Places</a> | 
              <a href=javascript:ajaxFunction('http://localhost:%s','/tags')>Tags</a> | 
              <a href=javascript:ajaxFunction('http://localhost:%s','/animals')>Animals</a></h3>
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
          <h2>Information</h2>
          <hr />
          <div class='scroller info large' id='info'></div>
        </div>
      </div>
      <div class='footer'>
        <a href='/site'><< Site Information</a> * %s v. %s. &copy; Martin Norling, AVID Project, ILRI, 2010 * <a href='/'>Sampling Page >></a>
      </div>
    </div>
  </body>
</html>
""" % (self.title, self.version, ajax_function(self.port), self.port, \
       site_style(), self.port, self.port, self.port, self.port, self.port, \
       self.port, self.title, self.version)
    
    def update(self, devices):
        output = ''
        output += ajax('position', position(devices['gps']))
        output += ajax('reader',   reader(devices['rfid']))
        return output
    
    def sample_types(self):
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
    
    def places(self):
        info  = '<table>'
        info += '<tr><th>Name</td><th>Latitude</td><th>Longtitude</td><th>Radius</td></tr>'
        for p in self.db.get_places():
            info += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % p
        info += '</table>'
        form  = 'Add Place:'
        form += '<table>'
        form += '<tr><th>Name</td><td><input type=\'text\' name=\'name\'></td><td></td></tr>'
        form += '<tr><th>Latitude</td><td><input type=\'text\' name=\'latitude\'></td><td></td></tr>'
        form += '<tr><th>Longtitude</td><td><input type=\'text\' name=\'longtitude\'></td><td></td></tr>'
        form += '<tr><th>Radius</td><td><input type=\'text\' name=\'radius\'></td><td>km</td></tr>'
        form += '</table>'
        return ajax('info', info) + ajax('input_form', form)
    
    def tags(self):
        info  = '<table>'
        info += '<tr><th>Label</td><th>RFID</td><th>Color</td><th>Supplier</td><th>Type</td></tr>' 
        for tag in self.db.get_tags():
            info += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tag
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
    
    def animals(self):
        info  = '<table>'
        info += '</table>'
        form  = 'Replace animal:<select name=\'replace\'>'
        for animal in self.db.get_animals():
            form += '<option name=\'%s\'>%s</option>' % (animal[0], animal[0])
        form += '</select><br>'
        form += 'Replace with:'
        form += '<table>'
        form += '</table>'
        return ajax('info', info) + ajax('input_form', form)
    
    def parse_form(self, form, info, devices):
        if 'prefix' in form:
            self.db.insert_prefix(form['prefix'][0], form['description'][0])
        elif 'radius' in form:
            self.db.insert_place(form['name'][0], form['latitude'][0], \
                                 form['longtitude'][0], form['radius'][0])
        elif 'rfid' in form:
            self.db.replace_tag(form['tag'][0], form['rfid'][0], \
                    form['color'][0], form['supplier'][0], form['tag_type'][0],\
                    form['replace'][0])
        return ''

import re

class SimplePage():
    def __init__(self, settings, db, devices, info):
        self.title = settings['name']
        self.version = settings['version']
        self.port = settings['port']
        self.info_time = settings['info_time']
        self.db = db
        self.devices = devices
        self.info = info
        self.gps = devices['gps']
    
    def update(self, info):
        output = ''
        output  = ajax('position', position(self.devices['gps']))
        return output

    def header(self):
        return """<html>
  <head>
    <title>%s v. %s - Admin</title>
    <script type=\'text/javascript\'>
    %s
""" % (self.title, self.version, ajax_function(self.port))

def ajax_function(port):
    return """
      function ajaxFunction(func,params)
      {
        var xmlhttp;
        if (window.XMLHttpRequest)
        {
          xmlhttp=new XMLHttpRequest();
        }
        else if (window.ActiveXObject)
        {
          xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange=function()
        {
          if(xmlhttp.readyState==4)
          {
            eval(xmlhttp.responseText);
          }
        }
      xmlhttp.open("GET", func+params, true);
      xmlhttp.send(null); 
      }
"""

def site_style():
    return """<style type='text/css'>
body {
  background-color: #fff;
  font-family: Trebuchet MS, Verdana;
  color: #fff;
  font-size: 1.3em
}
h1 {
  margin: 15px;
  text-align: center;
}
h2 {
  font-size: 1.2em;
  color: #fff;
  margin: 0 0 10px 0;
}
h3 {
  font-size: 0.9em;
  text-align: justify;
  margin: 5px;
}
a {
  text-decoration: none;
  color: #0f0;
}
.site {
  background-color: #9d9;
  width:980px;
  height: 530px;
  border: 1px solid #000;
  margin: 5px auto;
}
.box {
  background-color: #000;
  padding: 10px;
  width: 430px;
  border: 1px solid #fff;
}
.box.top {
  height: 80px;
}
.box.top table {
  margin: 10px 0 0 0;
  font-size: 0.9em;
}
.box.main {
  margin: 10px 0 0 0;
  height: 345px;
}
.left {
  float: left;
  margin: 10px 10px 10px 30px;
  width: 450px;
}
.right {
  float: right;
  margin: 10px 30px 10px 10px;
  width: 450px;
}
.footer {
  float: left;
  background-color: #000;
  margin: 0 30px 0 30px;
  padding: 5px;
  width: 910px;
  height: 10px;
  text-align: center;
  font-size: 0.5em;
  border: 1px solid #fff;
}
.scroller {
  overflow: auto;
  width: 420px;
  padding: 10px;
}
.info {
  height: 180px;
}
.large {
  height: 270px;
}
.error {
  color: #f00;
  height: 97px;
}
.input {
  height: 225px;
}
.submitbutton {
  text-align: right;
}
</style>
"""
                        
def ajax(target, value):
    value = sanitize(value)
    return 'document.getElementById("%s").innerHTML= "%s"; ' % (target,value)

def ajax_value(target, value):
    value = sanitize(value)
    return 'document.getElementById("%s").value = "%s"' % (target, value)

def sanitize(string):
    string = string.replace('\n','')
    return string

def position(gps):
    if gps.status == 'initializing':
        return '<div style=\'color: #f00;\'>Initializing</div>'
    if gps.status == 'Out of Sync':
        return '<div style=\'color: #ff0;\'>Out of Sync</div>'
    if gps.status == 'running':
        return '<div style=\'color: #0f0;\'>%s, %s, %s, %s(EAT)</div>' % (\
           gps_format(gps.data['latitude']), 
           gps_format(gps.data['longtitude']), 
           gps.data['altitude'],
           timeFormat(gps.data['time']))
    return '<div style=\'color: #f00;\'>Disconnected</div>'

def gps_format(pos):
	"""
	Formats the raw longitude or latitude
	"""
	output = pos
	if type(pos) == type(float()):
		output = '%+.6f' % pos
		output = output.zfill(10)
	return output

def timeFormat(rawTime):
	"""
	Formats the raw time received from the satellites
	"""
	formattedTime = rawTime[0:rawTime.index('.')]
	formattedTime = str(int(formattedTime[0:2]) + 3)  + ':' + formattedTime[2:4] + ':' + formattedTime[4:6]
	return formattedTime

def reader(rfid):
    color = '#f00'
    if rfid.status == 'connected':
        color = '#ff0'
    elif rfid.status == 'reading':
        color = '#0f0'
    return '<div style=\'color: %s;\'>%s</div>' % (color, rfid.name)


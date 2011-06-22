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

def ajax_function(port):
    return """
      function ajaxFunction(func,params)
      {
        
      }
"""

def site_style():
    return """<style type='text/css'>

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
	Formats the raw time received from the satellites to the EAT time.
	
	Receives the raw time from the satellites and converts it to a human readable time, in the 24Hr format
	Args:
		rawTime:	The raw time string as received from the satellites
	Returns:
		formattedTime:	The human readable formatted time
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

import re

class SimplePage():
    def __init__(self, settings, db, devices, info, logger):
        logger.info('Initializing the system settings')
        self.title = settings['name']
        self.version = settings['version']
        self.port = settings['port']
        self.info_time = settings['info_time']
        self.db = db
        self.devices = devices
        self.info = info
        self.gps = devices['gps']

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

def gpsPosition(gps):
    """
    Return the current GPS position
    """
    if gps.status == 'initializing':
        return "<div class='gps_initializing'>Initializing</div>"
    if gps.status == 'Out of Sync':
        return "<div class='gps_out_of_sync'>Out of Sync</div>"
    if gps.status == 'running':
        return "<div class='gps_running'>%s, %s, %s, %s(%s)</div>" % (\
            gps_format(gps.data['latitude']), 
            gps_format(gps.data['longtitude']), 
            gps.data['altitude'],
            gps.data['formattedTime'],
            gps.timeZoneName)
    return "<div class='gps_disconnected'>Disconnected</div>"

def gps_format(pos):
	"""
	Formats the raw longitude or latitude
	"""
	output = pos
	if type(pos) == type(float()):
		output = '%+.6f' % pos
		output = output.zfill(10)
	return output

def reader(rfid):
    color = '#f00'
    if rfid.status == 'connected':
        color = '#ff0'
    elif rfid.status == 'reading':
        color = '#0f0'
    return '<div style=\'color: %s;\'>%s</div>' % (color, rfid.name)

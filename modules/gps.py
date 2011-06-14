import threading
import serial
import re
import math
from time import time, sleep

class GPSReader(threading.Thread):
	""" @package GPS_Reader
	By: Martin Norling

	The GPS module
	"""
	
	## The Constructor
	def __init__(self, port, baud):
		threading.Thread.__init__(self)
		self.port     = port
		self.baud     = baud
		self.ports    = []
		self.OOS      = 30
		self.last     = time() - self.OOS
		self.timeout  = 1.5
		self.running  = True
		self.conn     = None
		self.distalgo = 'haversine'
		self.data = {'latitude':'N/A',   'longtitude':'N/A', 'altitude':'N/A', 
		'satellites':'N/A', 'dilution':'N/A',   'time':'<unknown>',
		'raw':''}
		self.gga = re.compile('\$GPGGA,([0-9.]+),([0-9.]+),(S|N),([0-9.]+),(E|W),\d,(\d+),([0-9.]+),([-0-9.]*),(M),[-0-9.]*,M,,0000\*...')

	def findGPSDongle(self):
		"""
		Find and starts reading from a gps dongle in /dev/
		"""
		self.data = {'latitude':'N/A', 'longtitude':'N/A', 'altitude':'N/A', 'satellites':'N/A', 'dilution':'N/A', 'time':'<unknown>'}
		if not self.ports:
			# scan the 'files' where the gps dongle is attached. In linux basically everything is a file
			for i in range(0,10):
				self.ports.append('%s%i' % (self.port, i))
		
		while not self.conn and self.running:
			self.status = 'initializing'
			for port in self.ports:
				try:
					sleep(0.1)
					self.conn = serial.Serial(port, self.baud, timeout = self.timeout)
					self.port = port
					self.last = time()
					break
				except:
					pass

	def stop(self):
		self.running = False

	def run(self):
		"""
		Reads a line from the GPS dongle and sets the self.data with the values read
		"""
		self.findGPSDongle()
		while self.running:
			try:
				if (self.last + self.OOS < time()):
					raise IOError
				elif self.data['latitude'] == 'N/A':
					self.status = 'Out of Sync'
				else:
					self.status = 'running'
				sleep(0.5)
				raw_data = self.conn.readline()
				match = self.gga.match(raw_data)
				
				if match:
					self.data['time'] = match.group(1)      
					self.data['latitude'] = self.convert(match.group(2))  
					self.data['longtitude'] = self.convert(match.group(4))
					self.data['satellites'] = match.group(6)
					self.data['dilution'] = match.group(7)
					self.data['raw'] = raw_data[:-2]
					
					if match.group(8):
						self.data['altitude'] = match.group(8)
					if match.group(3) == 'S':
						self.data['latitude'] = -self.data['latitude']
					if match.group(5) == 'W':
						self.data['longtitude'] = -self.data['longtitude']
						self.last = time()
			
			except Exception as e:
				print "Exception: %s" % e
				self.conn = None
				self.findGPSDongle()
				self.status = 'disconnected'

	def convert(self, coord):
		degrees = int(float(coord)/100)
		minutes = (float(coord)/100 % 1)*100
		return degrees + minutes/60

	def distance(self, lat, lon):
		distance = ''
		if not lat or not lon:
			return float('inf')
		if self.status == 'running':
			if self.distalgo == 'haversine':
				distance = self.haversine(lat, self.data['latitude'],
				lon, self.data['longtitude'])
			if self.distalgo == 'spherical law of cosines':
				distance = self.spherical_law_of_cosines(\
				lat, self.data['latitude'],
				lon, self.data['longtitude'])
			return distance

	def haversine(self, lat1, lat2, lon1, lon2):
		R = 6371.0
		rad = math.pi/180.0
		dLat = (lat2*rad - lat1*rad)
		dLon = (lon2*rad - lon1*rad)
		a = math.sin(dLat/2) * math.sin(dLat/2) + \
		math.cos(lat2*rad) * math.cos(lat1*rad) * \
		math.sin(dLon/2) * math.sin(dLon/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		return R *c

	def spherical_law_of_cosines(self, lat1, lat2, lon1, lon2):
		R = 6371.0
		rad = math.pi/180.0
		d = math.acos(math.sin(lat1*rad) * math.sin(lat2*rad) + \
		math.cos(lat1*rad) * math.cos(lat2*rad) * \
		math.cos(lon1*rad - lon2*rad)) * R
		return d

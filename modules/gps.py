# GPS Reader thread
# By: Martin Norling, ILRI, 2010
#

import threading
import serial
import re
from time import time, sleep

class GPSReader(threading.Thread):
    def __init__(self, port, baud):
        threading.Thread.__init__(self)
        self.port     = port
        self.baud     = baud
        self.ports    = []
        self.OOS      = 30
        self.last     = time() - self.OOS
        self.timeout  = 0.5
        self.running  = True
        self.conn     = None
        self.status   = ''
        self.gga = re.compile('\$GPGGA,([0-9.]+),([0-9.]+),(S|N),([0-9.]+),(E|W),\d,(\d+),([0-9.]+),([-0-9.]+),(M),[-0-9.]+,M,,0000\*...')
        self.unknown = {'latitude':'N/A', 'longtitude':'N/A', 'altitude':'N/A', \
                        'satellites':'N/A', 'dilution':'N/A', 'time':'<unknown>'}
        self.data = self.unknown

    def init(self):
        if self.ports == []:
            if re.match('[/a-zA-Z]+\d', self.port):
                self.ports = self.port
            else:
                for i in range(0,10):
                    self.ports.append('%s%i' % (self.port, i))
        
        while not self.conn and self.running:
            self.status = 'initializing'
            if (self.last + self.OOS < time()):
                self.data = self.unknown
            for port in self.ports: 
                try:
                    sleep(0.1)
                    self.conn = serial.Serial(port, self.baud, \
                                              timeout = self.timeout)
                    self.port = port
                    break
                except Exception as e:
                    pass
            
    def stop(self):
        self.running = False

    def run(self):
        self.init()
        while True and self.running:
            if (self.last + self.OOS < time()):
                self.status = 'Out of Sync'
                self.data = self.unknown
            else:
                self.status = 'running'
            try:
                if not self.conn.open():
                    sleep(1)
                    raw_data = self.conn.readline()
                    match = self.gga.match(raw_data)
                    if match:
                        # convert from degree, min, sec to degree
                        lat = '%s.%s' % (match.group(2)[0:2], \
                                         (10*int(match.group(2)[2:4] + \
                                                 match.group(2)[5:]))/6)
                        lon = '%s.%s' % (match.group(4)[0:3], \
                                         (10*int(match.group(4)[3:5] + \
                                                 match.group(4)[6:]))/6)
                        self.data = {'time':match.group(1),      \
                                     'latitude':lat,  \
                                     'longtitude':lon,\
                                     'satellites':match.group(6),\
                                     'dilution':match.group(7),  \
                                     'altitude':match.group(8)}
#4
                        if match.group(3) == 'S':
                            self.data['latitude'] = '-%s' % self.data['latitude']
                        if match.group(5) == 'W':
                            self.data['longtitude'] = '-%s' % self.data['longtitude']
                            
                        self.last = time()
                else:
                    raise IOError
            except:
                self.conn = None
                self.init()
        self.status = 'disconnected'

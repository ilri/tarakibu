#!/usr/bin/python2.6.6

import threading
import bluetooth
import re
from time import sleep

""" @package RFID_Reader
	By: Martin Norling, ILRI, 2010
	
	 Synchronizes and listens to an RFID device storing its output in the 
	 self.data. Built to use with the 'Stick Reader V3' RFID animal tag reader 
	 but might be able to be used with other RFID readers.
	
	 Takes a device dictionary as input on the format.
	 device = { 'name':<RFID common name>
	            'addr':None                # auto finds address
	            'connected':False          # defaults as False
"""	
class RFIDReader(threading.Thread):	

	## The class constructor
    def __init__(self, name, addr):
        threading.Thread.__init__(self)
        self.name = name
        self.addr = addr
        self.port = 1  # should be generated to unused port 1-30
        self.word = 21 # 
        self.running = True
        self.status = ''
        self.data = None
        self.pattern = re.compile('\w{2} (\d{3}) (\d{12})')
    
    def synchronize(self):
        self.status = 'synchronizing'
        while self.addr is None:
            if not self.running:
                break
            try:
                sleep(0.5)
                for address in bluetooth.discover_devices():
                    if bluetooth.lookup_name(address) == self.name:
                        self.addr = address
                        break
            except:
                pass
        if self.addr:
            self.status = 'connected'
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.bind(('',self.port))
            self.socket.connect((self.addr, self.port))
            self.socket.settimeout(1.0)
            self.status = 'reading'

    def stop(self):
        self.running = False        
        if self.addr:
            self.socket.close()
            self.status = 'disconnected'

    def run(self):
        global mode, active_tag
        mode = 'sample'
        self.synchronize()

        while self.running:
            try:
                temp = ''
                sleep(0.1)
                while len(temp) < self.word and self.running:
                    try:
                        temp += self.socket.recv(1024)
                    except bluetooth.BluetoothError as e:
                        if '%s' % e == 'timed out':
                            pass
                        else:
                            raise
                match = self.pattern.match(temp)
                if match and not self.data:
                    self.data = '%s%s' % (match.group(1), match.group(2))
            except IOError as e:
                self.socket.close()
                self.addr = None
                self.synchronize()

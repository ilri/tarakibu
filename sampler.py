#!/usr/bin/env python

import threading
import sys
import os
import MySQLdb
import cgi
from time import sleep, time
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from modules.rfid import RFIDReader
from modules.gps import GPSReader
from modules.sql import SamplerDb
from www.common import *
from www.simple import *
from www.admin import *
from www.site import *

settings = {'name'      :'Simple Sampler'                   ,
            'version'   :'0.8.2 BETA'                       ,
            'port'      :8080                               ,
            'db_host'   :'localhost'                        ,
            'db_name'   :'samples'                          ,
            'db_user'   :'samples'                          ,
            'db_pass'   :'54mpl35'                          ,
            'info_time' :10}
info     = {'mode'      :'animal'                           ,
            'target'    :'livestock'                        ,
            'active_tag':None                               ,
            'msg'       :'Welcome to %s!' % settings['name'],
            'error'     :''                                 ,
            'tag'       :None                               ,
            'tag_read'  :0,
            'farmer'    :''}

db       = SamplerDb(host   = settings['db_host'],
                     db     = settings['db_name'],
                     user   = settings['db_user'],
                     passwd = settings['db_pass'])

devices  = {'rfid':RFIDReader('Stick Reader V3', None),
            'gps' :GPSReader ('/dev/ttyUSB', 38400)}

pages    = {'simple':simple(settings, db, devices, info),
            'admin' :admin (settings, db, devices, info),
            'site'  :site  (settings, db, devices, info)}

class SamplerServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global pages, devices, settings, info
        try:
            sys.stderr = open(os.devnull,'w') # tell the server to shut up
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if self.path == '/':
                self.wfile.write(pages['simple'].site(info))
            else:
                path = self.path.split('/')
                if len(path) <= 2:
                    path.append('site')
                if len(path) > 3:
                    eval("self.wfile.write(pages[\'%s\'].%s('%s'))" % (path[1], path[2], "', '".join(path[3:])))
                else:
                    eval("self.wfile.write(pages[\'%s\'].%s(info))" % \
                             (path[1], path[2]))
        except IOError:
            self.send_error(404, 'File Not Found.')
    
    def do_POST(self):
        global pages, devices, settings, info,\
               mode, msg, active_tag, info, error
        try:
            ctype, pdict = cgi.parse_header(\
                           self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                self.send_response(301)
                form = cgi.parse_multipart(self.rfile, pdict)
                pages[form['page'][0]].parse_form(form, info, devices)
                self.send_header('Location', 'http://localhost:%s/%s' \
                                 % (settings['port'], form['page'][0]))
                self.end_headers()
        except IOError:
            self.send_error(501, 'Unsupported Method')

for device in devices:
    devices[device].start()

server = HTTPServer(('', settings['port']), SamplerServer)
print '* %s web server running on port %s.' % (settings['name'],\
                                               settings['port'])

try:
    server.serve_forever()
except:
    server.socket.close()

print '\n* Shutting down.'

for device in devices:
    devices[device].stop()
    devices[device].join()

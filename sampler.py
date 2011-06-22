#!/usr/bin/env python

import threading
import sys
import os
import MySQLdb
import cgi
import StringIO
from time import sleep, time
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from modules.rfid import RFIDReader
from modules.gps import GPSReader
from modules.sql import SamplerDb
from www.common import *
from www.simple import *
from www.admin import *
from www.site import *

## The basic settings for the simple sample
# We are including the absolute path to where the random sampler is located so that we can be able to include the files and the other
# resources that are need
settings = {'name'      :'Simple Sampler'                   ,
            'version'   :'0.8.2 BETA'                       ,
            'port'      :8080                               ,
            'db_host'   :'localhost'                        ,
            'absolute_path' : '/var/www/randomsampler'		,	#The absolute path to where the sampler is located
            'db_name'   :'dgea'                          ,
            'db_user'   :'root'                          ,
            'db_pass'   :'admin'                          ,
            'info_time' :10}
            
info     = {'mode'      :'animal'                           ,
            'target'    :'livestock'                        ,
            'active_tag':None                               ,
            'msg'       :'Welcome to %s!' % settings['name'],
            'error'     :''                                 ,
            'tag'       :None                               ,
            'tag_read'  :0,
            'farmer'    :''}

## The database settings
db       = SamplerDb(host   = settings['db_host'],
                     db     = settings['db_name'],
                     user   = settings['db_user'],
                     passwd = settings['db_pass'])

## All the devices that we want to be loaded
devices  = {'gps' :GPSReader ('/dev/ttyUSB', 4800)}

## The pages that will be created by the sampler
pages = {'simple':simple(settings, db, devices, info),
            'admin' :admin (settings, db, devices, info),
            'site'  :site  (settings, db, devices, info)}

class SamplerServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global pages, devices, settings, info
        try:
			#sys.stderr = open('error.log','a') # tell the server to shut up
            pathMatch = re.match( r'/resource(.*)', self.path, re.M|re.I)
            if pathMatch != None:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
            path = self.path.split('/')
			
            if self.path == '/':
                self.wfile.write(pages['simple'].site(info))
            else:
                pathMatch = re.match( r'/resource\?(.*)', self.path, re.M|re.I)
                #print path
                #print pathMatch
                if pathMatch != None:
					#we are requesting for a file, it can be a javascript, css or just a plain text file 
					#jst read the whole file and output it
					try:
						f = open(pathMatch.group(1), "rt")
					except IOError:
						self.send_error(404, 'Requested file %s not found.' % pathMatch.group(1))
						return
					self.wfile.write(f.read())
					f.close()
					return
                elif len(path) <= 2:
                    path.append('site')
                elif len(path) > 3:
                    eval("self.wfile.write(pages[\'%s\'].%s('%s'))" % (path[1], path[2], "', '".join(path[3:])))
                else:
                    eval("self.wfile.write(pages[\'%s\'].%s(info))" % (path[1], path[2]))
        except IOError:
            self.send_error(404, 'File Not Found.')
    
    def do_POST(self):
        global pages, devices, settings, info, mode, msg, active_tag, info, error
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                self.send_response(301)
                form = cgi.parse_multipart(self.rfile, pdict)
                pages[form['page'][0]].parse_form(form, info, devices)
                self.send_header('Location', 'http://localhost:%s/%s' % (settings['port'], form['page'][0]))
                self.end_headers()
        except IOError:
            self.send_error(501, 'Unsupported Method')

## Start all the devices that need to be started
for device in devices:
    devices[device].start()		#Call the respective threads

server = HTTPServer(('', settings['port']), SamplerServer)
print '* %s web server running on port %s.' % (settings['name'], settings['port'])

try:
    server.serve_forever()
except:
    server.socket.close()

print '\n* Shutting down.'

for device in devices:
    devices[device].stop()
    devices[device].join()

#!/usr/bin/env python

import threading
import sys
import os
import MySQLdb
import math
import logging
import StringIO
from time import sleep, time
import cgi
#import cgitb
#cgitb.enable(display=1, logdir="log")
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from modules.gps import GPSReader
from modules.sql import SamplerDb
from www.common import *
from www.simple import *
from www.admin import *
from www.site import *

## The basic settings for the simple sample
# We are including the absolute path to where the random sampler is located so that we can be able to include the files and the other
# resources that are need
settings = {'name'          :'Simple Sampler'                   ,
            'version'       :'0.8.2 BETA'                       ,
            'port'          :8080                               ,
            'timeZone'      :+3                                 ,   #The time zone where the sampling is taking place. This is the number of hours before or after the GMT
            'timeZoneName'  :'EAT'                              ,   #The name of the time zone that we are currently operating in
            'db_host'       :'localhost'                        ,
            'absolute_path' : '/var/www/randomsampler'		    ,	#The absolute path to where the sampler is located
            'db_name'       :'dgea'                             ,
            'db_user'       :'root'                             ,
            'barcode_use'   :'yes'                              ,   #shall we be using barcoded samples and aliquots in this sampling trip?
            'db_pass'       :'admin'                            ,
            'info_time'     :10}
            
info     = {'mode'      :'animal'                           ,
            'target'    :'dgea'                             ,
            'active_tag':None                               ,
            'msg'       :'Welcome to %s!' % settings['name'],
            'error'     :''                                 ,
            'tag'       :None                               ,
            'tag_read'  :0,
            'farmer'    :''}

#start the logging facility, bt first ensure that the log file exits or the path exists and is accessible
if not os.path.exists('log'):
	os.makedirs('log')
if not os.path.exists('log/dgea_sampler.log'):
	FILE = open('log/dgea_sampler.log', 'w')
	FILE.close()
		
logger = logging.getLogger('DGEA_Sampler')
logHandler = logging.FileHandler('log/dgea_sampler.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
logger.info('A new session has been started')

## The database settings
db       = SamplerDb(host   = settings['db_host'],
                     db     = settings['db_name'],
                     user   = settings['db_user'],
                     passwd = settings['db_pass'])

## All the devices that we want to be loaded
devices  = {'gps' :GPSReader ('/dev/ttyUSB', logger, 4800, settings['timeZone'], settings['timeZoneName'])}

## The pages that will be created by the sampler
pages = {'simple':simple(settings, db, devices, info, logger),
            'admin' :admin (settings, db, devices, info, logger),
            'site'  :site  (settings, db, devices, info, logger)}

class SamplerServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global pages, devices, settings, info
        try:
            #sys.stderr = open('error.log','a') # tell the server to shut up
            #print self.path
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
        """
        The main function that will handle all the POST requests. The inclusion of global variables is ugly, but at this point I will leave it at that
        
        @todo Remove the global variables
        @todo Check for GPS validity at this stage instead of later on in the program
        """
        global pages, devices, settings
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                #print postvars
                #print self.path
                #now call the function that is meant to process this request
                if(self.path == '/simple/selectedHousehold'):
                    print 'need to get all cows in household #%s ' % postvars['household'][0]
                    output = pages[postvars['page'][0]].selectedHousehold(postvars['household'][0], devices)
                    self.wfile.write(output)
                if(self.path == '/simple/nextAnimal'):
                    print 'we have finalized saving samples for one animal, now we need to go to the next animal'
                    output = pages[postvars['page'][0]].nextAnimal(postvars, devices)
                    self.wfile.write(output)
                elif(self.path == '/simple/sampleCow'):
                    print 'we sampling the cow'
                    #we have the cow that we want to sample...now proceed with the sampling
                    output = pages[postvars['page'][0]].collectSample(postvars, devices)
                    self.wfile.write(output)
                elif(self.path == '/simple/saveSample'):
                    print 'we saving a new sample'
                    #the user have entered a sample for an animal
                    output = pages[postvars['page'][0]].saveSample(postvars, devices, settings['barcode_use'])
                    self.wfile.write(output)
                elif(self.path == '/simple/updateGPSCoordinates'):
                    #we want to get the current GPS position
                    output = pages[postvars['page'][0]].curPosition(devices['gps'])         #for the sake of consistence, we just using the passed 'page' variable
                    self.wfile.write(output)
                elif(self.path == '/simple/deleteSample'):
                    print 'we need to delete the sample %s ' % postvars['sample'][0]
                    #the user have entered a sample for an animal
                    output = pages[postvars['page'][0]].deleteSample(postvars['sample'][0], devices)
                    self.wfile.write(output)
                elif(self.path == '/simple/deleteAnimal'):
                    print postvars
                    print 'we need to delete the animal %s ' % postvars['curAnimalRead'][0]
                    #the user have entered a sample for an animal
                    output = pages[postvars['page'][0]].deleteAnimal(postvars['curAnimalRead'][0], devices)
                    self.wfile.write(output)
                    
            if ctype == 'multipart/form-data':
                self.send_response(301)
                form = cgi.parse_multipart(self.rfile, pdict)
                print form
                pages[form['page'][0]].parse_form(form, info, devices)
                self.send_header('Location', 'http://localhost:%s/%s' % (settings['port'], form['page'][0]))
                self.end_headers()
        except IOError:
            self.send_error(501, 'Unsupported Method')

class StreamFilter( object ):
    """
    Filters a data stream according to a number of rules.
    """
    def __init__( self, out_stream = sys.stdout ):
        """
        Initializes a stream filter, basically does imports and compiles regexes
        """
        import re
        self.out_stream = out_stream
        self.GET = re.compile('.*GET.*')
    
    def write( self, s ):
        """
        Writes a filtered message to stdout.
        """
        match = self.GET.match( s )
        if match:
            self.out_stream.write( s )
sys.stderr = StreamFilter()


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

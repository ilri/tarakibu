#!/usr/bin/env python

"""
 Copyright 2011 ILRI
 
 This file is part of tarakibu.
 
 tarakibu is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 tarakibu is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with tarakibu.  If not, see <http://www.gnu.org/licenses/>.
 
"""

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
settings = {'name'          :'tarakibu'                         ,
            'version'       :'0.1 BETA'                         ,
            'port'          :8080                               ,
            'radius'        :200                                ,   #The radius in which households shall fall in
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
            'error'     :''
            ,
            'tag'       :None                               ,
            'tag_read'  :0,
            'farmer'    :''}

#start the logging facility, bt first ensure that the log file exits or the path exists and is accessible
if not os.path.exists('log'):
	os.makedirs('log')
if not os.path.exists('log/tarakibu.log'):
	FILE = open('log/dgea_sampler.log', 'w')
	FILE.close()
		
logger = logging.getLogger('tarakibu')
logHandler = logging.FileHandler('log/tarakibu.log')
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
            'summary'  :summary  (settings, db, devices, info, logger)}

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
                self.wfile.write(pages['simple'].site(info, devices['gps']))
            elif(self.path == '/admin'):
                self.wfile.write(pages['admin'].site(info))
            elif(self.path == '/summary'):
                self.wfile.write(pages['summary'].site(info))
            else:
                pathMatch = re.match( r'/resource\?(.*)', self.path, re.M|re.I)
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
                #if(self.path != '/simple/updateGPSCoordinates'):
                    #print postvars
                #print self.path
                #now call the function that is meant to process this request
                if(self.path == '/simple/selectedHousehold'):
                    #print 'need to get all cows in household #%s ' % postvars['household'][0]
                    output = pages[postvars['page'][0]].selectedHousehold(postvars['household'][0], devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/selectedSite'):
                    #print 'need to get all the households from the site #%s ' % postvars['sites'][0]
                    output = pages[postvars['page'][0]].selectedSite(postvars['sites'][0], devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/nextAnimal'):
                    #print 'we have finalized saving samples for one animal, now we need to go to the next animal'
                    output = pages[postvars['page'][0]].nextAnimal(postvars, devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/sampleCow'):
                    #print 'we sampling the cow'
                    #we have the cow that we want to sample...now proceed with the sampling
                    output = pages[postvars['page'][0]].collectSample(postvars, devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/saveSample'):
                    #print 'we saving a new sample'
                    #the user have entered a sample for an animal
                    output = pages[postvars['page'][0]].saveSample(postvars, devices['gps'], settings['barcode_use'])
                    self.wfile.write(output)
                elif(self.path == '/simple/updateGPSCoordinates'):
                    #we want to get the current GPS position
                    output = pages[postvars['page'][0]].curPosition(devices['gps'])         #for the sake of consistence, we just using the passed 'page' variable
                    self.wfile.write(output)
                elif(self.path == '/simple/deleteSample'):
                    #print 'we need to delete the sample %s ' % postvars['sample'][0]
                    #the user have entered a sample for an animal
                    output = pages[postvars['page'][0]].deleteSample(postvars['sample'][0], devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/deleteAnimal'):
                    #print postvars
                    #print 'we need to delete the anial %s ' % postvars['curAnimalRead'][0]
                    #the user have entered a sample for an animal
                    output = pages[postvars['page'][0]].deleteAnimal(postvars['curAnimalRead'][0], devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/showAllSites'):
                    #print postvars
                    #print 'we either to show all sites or just the households within a certain radius'
                    #the user have entered a sample for an animal
                    output = pages[postvars['page'][0]].showSites(postvars, devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/refreshSampler'):
                    #print 'I really dont know what to do here, so we shall evaluate it a case on case basis'
                    output = pages[postvars['page'][0]].refreshSampler(postvars, devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/simple/updateHouseholds'):
                    #print 'The radius of interest has changed...lets update the households'
                    output = pages[postvars['page'][0]].updateSites(postvars, devices['gps'])
                    self.wfile.write(output)
                elif(self.path == '/admin'):
                    #print 'admin page'
                    
            if ctype == 'multipart/form-data':
                self.send_response(301)
                form = cgi.parse_multipart(self.rfile, pdict)
                #print form
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

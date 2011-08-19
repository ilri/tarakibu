"""
 Copyright 2011 ILRI
 
 This file is part of <ex simple sampler>.
 
 <ex simple sampler> is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 <ex simple sampler> is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with <ex simple sampler>.  If not, see <http://www.gnu.org/licenses/>.
 
"""

import MySQLdb
import re

class SamplerDb():
    def __init__(self, host, user, passwd, db):
        self.error = None
        self.host = host
        self.usr  = user
        self.pwd  = passwd
        self.db   = db
        self.curQuery = ''
    
    def _query(self, query):
        """
        Initialize a connection to the database and execute any query that needs execution
        """
        try:
            connection = MySQLdb.connect(user = self.usr,  passwd = self.pwd, host = self.host, db = self.db)
            db = connection.cursor()
        except:
            print 'Exception: Could not connect to Database'
            raise
        #now lets execute the passed query
        #print query
        try:
            db.execute(query)
            self.lastInsertId = connection.insert_id()
            connection.commit()
            #get all the data as a dictionary
            return db.fetchall()
        
        except:
            print 'Exception: Malformed Query "%s"' % query
            raise
    
    def dictQuery(self):
        """
        Returns a dictionary as the results instead of a tuple
        """
        try:
            connection = MySQLdb.connect(user = self.usr,  passwd = self.pwd, host = self.host, db = self.db)
            db = connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print 'Exception: Could not connect to Database'
            raise
        #print query
        try:
            db.execute(self.curQuery)
            #get all the data as a dictionary
            return db.fetchall()
        
        except:
            print 'Exception: Malformed Query "%s"' % query
            raise
    
    def isBarcodePrefixDefined(self, barcode):
        """
        Checks whether the prefix of the barcode is defined in the database or we have an alien sample
        """
        barcode = barcode.upper()
        for prefix_test in self._query('SELECT prefix FROM sample_types;'):
            if barcode.startswith(prefix_test[0]):
                return 0
        return 1    #we dont have that prefix defined...returned 1


# -- Kihara's modifications

    def getHouseholds(self):
        """
        Get all the households that are in the selected site
        """
        output = []
        data = self._query('SELECT hhid, id, latitude, longitude FROM households;')
        if data:
            for household in data:
                output.append(household)
        return output

    def getHouseholdCattle(self, householdId):
        """
        Get all the cattle in the selected household
        """
        output = []
        householdCattle = self._query("SELECT id, name FROM animals where hhId = %d ORDER BY name ASC;" % int(householdId))
        for cattle in householdCattle:
            output.append(cattle)
        return output

    def getSiteHouseholds(self, siteId):
        """
        Get all the households in the selected site
        """
        output = []
        siteHouseholds = self._query("SELECT hhid, id FROM households where siteId = %d ORDER BY hhid ASC;" % int(siteId))
        for household in siteHouseholds:
            output.append(household)
        return output
    
    def getSites(self):
        """
        Get all the sites
        """
        return self._query('SELECT id, name FROM sites ORDER BY name ASC;');

    def logGpsData(self, gpsData):
        """
        Logs the gps data at this current instance and returns the id of the logged GPS data
        """
        dateTime = gpsData['date'] + ' ' + gpsData['formattedTime']
        self._query('INSERT INTO gps_data(read_time, latitude, longitude, altitude, satellites, hdop, raw_data)  \
                     VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                    (dateTime, gpsData['latitude'], gpsData['longitude'], gpsData['altitude'], gpsData['satellites'], gpsData['dilution'], gpsData['raw']))
        return self.lastInsertId
    

    def logAnimalRead(self, gpsId, animalId, event):
        """
        We have 'read' an animal in the aim of bleeding it, so lets log this event
        """
        self._query("insert into animal_reads(animalId, gps_id, action) values(%s, %s, '%s')" % (animalId, gpsId, event))
        return self.lastInsertId


    def logSampleRead(self, barcode, gpsId, action):
        """
        Logs a sample read. A sample was scanned for whichever purpose. This is for the sake of trace-ability
        """
        self._query("insert into sample_reads(barcode, gps_id, action) values('%s', '%s', '%s')" % (barcode, gpsId, action))


    def get_location(self, gps):
        location = ''
        for place in self.get_places():
            if place and gps.distance(place[1], place[2]) < place[3]:
                location = place[0]
                break
        return location


    def get_village_info(self, village):
        query = 'SELECT village, province, district FROM place_infos WHERE village = "%s";' % village
        return self._query(query)
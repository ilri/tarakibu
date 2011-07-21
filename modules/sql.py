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
        if not prefix:
            return 1

    def tag_to_label(self, tag):
        return self._query('SELECT label FROM active_tags \
                                   WHERE rfid = "%s";' % tag)[0]

    def tag_to_id(self, tag):
        return self._query('SELECT id FROM tag_reads \
                                   WHERE rfid = "%s" \
                                   ORDER BY read_time DESC LIMIT 1;' % tag.upper())[0]

    def verify_sample(self, barcode):
        prefix = self._query('SELECT prefix FROM sample_types;')
        for test in prefix:
            if test[0] == barcode[:len(test[0])].upper() and len(barcode) == 9:
                if self._query('SELECT barcode FROM samples WHERE barcode="%s" AND prefix="%s";' \
						% (barcode[len(test[0]):],barcode[:len(test[0])].upper())):
                    return False
                return True
        return False

    def verify_tag(self, tag):
        return self._query('SELECT DISTINCT(label) FROM (SELECT label FROM tags UNION SELECT tag FROM animals) AS label WHERE label NOT IN (SELECT label FROM tag_replacements) AND label = "%s";' % tag)

    def insert_tag_read(self, tag, pos):
        self._query('INSERT INTO tag_reads                     \
                            (rfid,     latitude,   longitude, \
                             altitude, satellites, hdop, raw_data)  \
                     VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");' % \
                            (tag.upper(), pos['latitude'], pos['longitude'],\
                                  pos['altitude'], pos['satellites'],\
                                  pos['dilution'], pos['raw']))

    def insert_sample(self, barcode, tag, pos, info):
        tag_read = self.tag_to_id(tag)[0]
        prefix, barcode = self.split_barcode(barcode)
        self._query('INSERT INTO samples (prefix,     barcode,    tag_read, \
                                          latitude,   longitude, altitude, \
                                          satellites, hdop,   comment, raw_data) \
                     VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s", "%s");' % \
                            (prefix, barcode, tag_read, 
                             pos['latitude'], pos['longitude'], 
                             pos['altitude'], pos['satellites'],
                             pos['dilution'], info, pos['raw']))
    
    def get_samples(self, rfid):
        tag_read = self.tag_to_id(rfid)
        output = {}
        data = self._query('SELECT prefix FROM samples WHERE tag_read = "%s";'\
                           % tag_read)
        for prefix in data:
            output[prefix[0]] = data.count(prefix)
        return output
    
    def sample_info(self, tag):
        limit = 20
        info = 'No Sample Information Available'
        if tag:
            info  = 'Animal %s<hr />Latest Samples:<br />' % tag.upper()
            info += '<table>'
            for sample in self._query(\
               'SELECT prefix, barcode, sample_time FROM samples        \
                       WHERE tag_read IN                                \
                            (SELECT id FROM tag_reads WHERE rfid = "%s" \
                                       ORDER BY read_time ASC)          \
                       ORDER BY sample_time DESC LIMIT %s;' % (tag,limit)):
                info += '<tr><td>%s%s</td><td>%s</td></tr>' % \
                    (sample[0], sample[1], sample[2])
            info += '</table>'
        return info
    
    def get_sample_types(self):
        output = []
        data = self._query('SELECT prefix, description FROM sample_types;')
        if data:
            for sample_type in data:
                output.append(sample_type)
        return output 
    
    def get_tags(self):
        output = []
        data = self._query('SELECT label,rfid,color,supplier,type \
                                   FROM active_tags ORDER BY label;')
        if data:
            for tag in data:
                output.append(tag)
        return output
    
    def insert_prefix(self, prefix, description):
        prefix = prefix.upper()
        self._query('INSERT INTO sample_types(prefix, description) \
                            VALUES ("%s", "%s");' % (prefix, description))

    def get_places(self):
        output = []
        data = self._query('SELECT name, latitude, longitude, radius \
                                   FROM places ORDER BY name')
        if data:
            for place in data:
                output.append(place)
        return output
    
    def insert_place(self, name, latitude, longitude, radius):
        if latitude == 'N/A':
            latitude = 'NULL'
        if longitude == 'N/A':
            longitude = 'NULL'
        query = 'INSERT INTO places(name, latitude, longitude, radius) VALUES ("%s",%s,%s,%s);' % (name, latitude, longitude, radius)
        self._query(query)

    def replace_tag(self, tag, rfid, color, supplier, tag_type, replace):
        self._query('INSERT INTO tag_replacements                          \
                            (rfid, label, color, supplier, type, replaces) \
                            VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' %\
                            (rfid, tag.upper(), color, supplier, tag_type, 
                             replace.upper()))
    
    def get_animals(self):
        output = []
        data = self._query('SELECT tag,sex,owner,location FROM active_animals;')
        if data:
            for animal in data:
                output.append(animal)
        return output
    
    def get_latest_samples(self):
        output = []
        data = self._query('SELECT barcode, sample_time, comment \
                                   FROM active_samples           \
                                   ORDER BY sample_time DESC LIMIT 50;')
        if data:
            for sample in data:
                output.append(sample)
        return output
    
    def update_samples(self, tag, info):
        prefix = ''
        for prefix_test in self._query('SELECT prefix FROM sample_types;'):
            if tag.startswith(prefix_test[0]):
                prefix = prefix_test[0]
                break
        if not prefix:
            raise Exception('Unknown prefix')
        barcode = tag[len(prefix):]
        self._query('UPDATE samples SET comment = "%s"                 \
                            WHERE prefix = "%s" AND barcode = "%s";' % \
                           (info[0][1], prefix, barcode))
        if info[1][1]:
            self._query('INSERT INTO deleted_samples(prefix, barcode) \
                                   VALUES ("%s", "%s");' % (prefix, barcode))
    
    def get_animals_at_location(self, location):
        output = []
        data = self._query('SELECT tag, sex, owner, location, sampled \
                                   FROM recently_sampled              \
                                   WHERE location = "%s" ORDER BY owner;'\
                               % location)
        if data:
            for animal in data:
                output.append(animal)
        return output
    
    def replace_animal(self, replace, new_tag, date_of_birth, 
                       sex,  owner,   weight,  comment):
        self._query('INSERT INTO animals (tag, date_of_birth, sex, owner) \
                            VALUES ("%s", "%s", "%s", "%s");' %           \
                           (new_tag, date_of_birth, sex, owner))
        self._query('INSERT INTO animal_measures (animal, weight, comment)\
                            VALUES ("%s", "%s", "%s");' %                 \
                           (new_tag, weight, comment))
        self._query('INSERT INTO animal_replacements                      \
                            (new_animal, replaces_animal)                 \
                            VALUES ("%s", "%s");' %                       \
                           (new_tag, replace))
    
    def get_next_animal_id(self, location, species):
        length = len(location) + len(species) + 3
        next = self._query('SELECT MAX(CAST(SUBSTR(tag FROM %i) AS UNSIGNED)) + 1 AS num FROM animals WHERE species = "%s" AND location = "%s";' % (length, species, location))[0][0]
        if not next:
            next = 1
        return '%s/%s/%03i' % (location, species, next)
    
    def input_random_animal(self, form):
        try:
            self._query('INSERT INTO animals (tag, sex, species, owner, location) VALUES ("%s", "%s", "%s", "%s", "%s");' % (form['animal_id'][0], form['sex'][0], form['species'][0], form['owner'][0], form['location'][0]))
            self._query('INSERT INTO animal_measures (animal, approximate_age, rvf_vaccine, vaccines, comment) VALUES ("%s", "%s", "%s", "%s", "%s");' % (form['animal_id'][0], form['age'][0], form['rvf'][0], form['vaccines'][0], form['comment'][0]))
        except:
            raise
        return True

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
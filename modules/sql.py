
import MySQLdb
import re

class SamplerDb():
    def __init__(self, host, user, passwd, db):
        self.error = None
        try:
            self.host = host
            self.usr  = user
            self.pwd  = passwd
            self.db   = db
        except:
            raise
    
    def _query(self, query):
        try:
            connection = MySQLdb.connect(user = self.usr,  passwd = self.pwd,
                                         host = self.host, db     = self.db)
            db = connection.cursor()
        except:
            print 'Exception: Could not connect to Database'
            raise
        try:
            db.execute(query)
            return db.fetchall()
        except:
            print 'Exception: Malformed Query "%s"' % query
            raise
    
    def split_barcode(self, barcode):
        barcode = barcode.upper()
        prefix = ''
        for prefix_test in self._query('SELECT prefix FROM sample_types;'):
            if barcode.startswith(prefix_test[0]):
                prefix = prefix_test[0].upper()
                break
        if not prefix:
            raise Exception('Unknown prefix')
        barcode = barcode[len(prefix):]
        return prefix, barcode

    def tag_to_label(self, tag):
        return self._query('SELECT label FROM active_tags \
                                   WHERE rfid = "%s";' % tag)

    def tag_to_id(self, tag):
        return self._query('SELECT id FROM tag_reads \
                                   WHERE rfid = "%s" \
                                   ORDER BY read_time DESC LIMIT 1;' % tag.upper())[0]

    def verify_sample(self, barcode):
        prefix = self._query('SELECT prefix FROM sample_types;')
        for test in prefix:
            if test[0] == barcode[:len(test[0])].upper() and len(barcode) == 9:
                if self._query('SELECT barcode FROM samples \
                                       WHERE barcode="%s" AND prefix="%s";' % \
                                      (barcode[len(test[0]):],
                                       barcode[:len(test[0])].upper())):
                    return False
                return True
        return False

    def verify_tag(self, tag):
        return self._query('SELECT DISTINCT(label) FROM (SELECT label FROM tags UNION SELECT tag FROM animals) AS label WHERE label NOT IN (SELECT label FROM tag_replacements) AND label = "%s";' % tag)

    def insert_tag_read(self, tag, pos):
        self._query('INSERT INTO tag_reads                     \
                            (rfid,     latitude,   longtitude, \
                             altitude, satellites, hdop, raw_data)  \
                     VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");' % \
                            (tag.upper(), pos['latitude'], pos['longtitude'],\
                                  pos['altitude'], pos['satellites'],\
                                  pos['dilution'], pos['raw']))

    def insert_sample(self, barcode, tag, pos, info):
        tag_read = self.tag_to_id(tag)[0]
        prefix, barcode = self.split_barcode(barcode)
        self._query('INSERT INTO samples (prefix,     barcode,    tag_read, \
                                          latitude,   longtitude, altitude, \
                                          satellites, hdop,   comment, raw_data) \
                     VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s", "%s");' % \
                            (prefix, barcode, tag_read, 
                             pos['latitude'], pos['longtitude'], 
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
        else:
            output.append(('Could not load','sample types'))
        return output 
    
    def get_tags(self):
        output = []
        data = self._query('SELECT label,rfid,color,supplier,type \
                                   FROM active_tags ORDER BY label;')
        if data:
            for tag in data:
                output.append(tag)
        else:
            output.append(('Could','not','load','tags',''))
        return output
    
    def insert_prefix(self, prefix, description):
        prefix = prefix.upper()
        self._query('INSERT INTO sample_types(prefix, description) \
                            VALUES ("%s", "%s");' % (prefix, description))

    def get_places(self):
        output = []
        data = self._query('SELECT name, latitude, longtitude, radius \
                                   FROM places ORDER BY name')
        if data:
            for place in data:
                output.append(place)
        else:
            output.append(('Could','not','load','places'))
        return output
    
    def insert_place(self, name, latitude, longtitude, radius):
        self._query('INSERT INTO places(name, latitude, longtitude, radius) \
                            VALUES ("%s",%s,%s,%s);' % \
                           (name, latitude, longtitude, radius))

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
        else:
            output.append(('Could','not','load','animals'))
        return output
    
    def get_latest_samples(self):
        output = []
        data = self._query('SELECT barcode, sample_time, comment \
                                   FROM active_samples           \
                                   ORDER BY sample_time DESC LIMIT 50;')
        if data:
            for sample in data:
                output.append(sample)
        else:
            output.append(('Could not','load','latest','samples'))
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
        else:
            output.append(('Could','not','load','animals', False))
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
    
    def get_next_animal_id(self):
        next = self._query('SELECT MAX(CAST(SUBSTR(tag FROM 4) AS UNSIGNED)) + 1 AS max FROM animals;')[0][0]
        if not next:
            next = 1000
        return 'AVD%s' % next
    
    def input_random_animal(self, form):
        try:
            self._query('INSERT INTO animals (tag, sex, species, owner, location) VALUES ("%s", "%s", "%s", "%s", "%s");' % (form['animal_id'][0], form['sex'][0], form['species'][0], form['owner'][0], form['location'][0]))
            self._query('INSERT INTO animal_measures (animal, approximate_age, comment) VALUES ("%s", "%s", "%s");' % (form['animal_id'][0], form['age'][0], form['comment'][0]))
        except:
            raise
        return True

    def get_species(self):
        return self._query('SELECT common_name FROM species ORDER BY common_name DESC;');

    def get_location(self, gps):
        location = ''
        for place in self.get_places():
            if gps.distance(place[1], place[2]) < place[3]:
                location = place[0]
                break
        return location

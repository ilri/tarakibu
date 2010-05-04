
import MySQLdb
import re

class SamplerDb():
    def __init__(self, host, user, passwd, db):
        self.error = None
        self.prefixpattern = re.compile('([a-zA-Z])*')
        try:
            self.conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
            self.db = self.conn.cursor()
        except:
            raise
    
    def tag_to_label(self, tag):
        self.db.execute('SELECT label FROM active_tags WHERE rfid = "%s";' % tag)
        return self.db.fetchone()

    def tag_to_id(self, tag):
        self.db.execute('SELECT id FROM tag_reads WHERE rfid = "%s" ORDER BY read_time DESC LIMIT 1;' % tag)
        return self.db.fetchone()[0]

    def verify_sample(self, barcode):
        self.db.execute('SELECT prefix FROM sample_types;')
        prefix = self.db.fetchall()
        for test in prefix:
            if test[0] == barcode[:len(test[0])].upper() and len(barcode) == 9:
                self.db.execute('SELECT barcode FROM samples WHERE barcode="%s" AND prefix="%s";' % (barcode[3:], barcode[:3].upper()))
                if self.db.fetchone():
                    return False
                return True
        return False

    def verify_tag(self, tag):
        self.db.execute('SELECT label FROM active_tags WHERE label="%s";' % tag)
        return self.db.fetchone()

    def insert_tag_read(self, tag, pos):
        self.db.execute('INSERT INTO tag_reads (rfid, latitude, longtitude, altitude, satellites, hdop) VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' % (tag, pos['latitude'], pos['longtitude'], pos['altitude'], pos['satellites'], pos['dilution']))

    def insert_sample(self, barcode, tag, pos, info):
        tag_read = self.tag_to_id(tag)
        try:
            self.db.execute('INSERT INTO samples (prefix, barcode, tag_read, latitude, longtitude, altitude, satellites, hdop, comment) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (barcode[0:3].upper(), barcode[3:], tag_read, pos['latitude'], pos['longtitude'], pos['altitude'], pos['satellites'], pos['dilution'], info))
        except Exception as e:
            print e
            self.error = 'Could not insert sample. Returned %s' % e
    
    def get_samples(self, rfid):
        tag_read = self.tag_to_id(rfid)
        self.db.execute('SELECT prefix FROM samples WHERE tag_read = "%s";'\
                         % tag_read)
        output = {}
        data = self.db.fetchall()
        for prefix in data:
            output[prefix[0]] = data.count(prefix)

        return output
    
    def sample_info(self, tag):
        limit = 20
        info = 'No Sample Information Available'
        if tag:
            info = 'Animal %s<hr />Latest Samples:<br />' % tag.upper()
            try:
                self.db.execute('SELECT prefix, barcode, sample_time FROM samples WHERE tag_read IN (SELECT id FROM tag_reads WHERE rfid = "%s" ORDER BY read_time ASC) ORDER BY sample_time DESC LIMIT %s;' % (tag,limit))
                info += '<table>'
                for sample in self.db.fetchall():
                    info += '<tr><td>%s%s</td><td>%s</td></tr>' % \
                             (sample[0], sample[1], sample[2])
                info += '</table>'
            except Exception as e:
                print e 
        return info
    
    def get_sample_types(self):
        output = []
        try:
            self.db.execute('SELECT prefix, description FROM sample_types;')
            data = self.db.fetchall()
            for sample_type in data:
                output.append(sample_type)
        except:
            output.append('Could not load sample types')
        return output 
    
    def get_tags(self):
        output = []
        try:
            self.db.execute('SELECT label,rfid,color,supplier,type FROM active_tags ORDER BY label;')
            for tag in self.db.fetchall():
                output.append(tag)
        except:
            output.append('Could not load tags')
        return output
    
    def insert_prefix(self, prefix, description):
        prefix = prefix.upper()
        self.db.execute('INSERT INTO sample_types(prefix, description) VALUES ("%s", "%s");' % (prefix, description))

    def get_places(self):
        output = []
        try:
            self.db.execute('SELECT name, latitude, longtitude, radius FROM places ORDER BY name')
            for place in self.db.fetchall():
                output.append(place)
        except:
            output.append('Could not load places')
        return output
    
    def insert_place(self, name, latitude, longtitude, radius):
        self.db.execute('INSERT INTO places(name, latitude, longtitude, radius) VALUES ("%s",%s,%s,%s);' % (name, latitude, longtitude, radius))

    def replace_tag(self, tag, rfid, color, supplier, tag_type, replace):
        query = 'INSERT INTO tag_replacements (rfid, label, color, supplier, type, replaces) VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' % (rfid, tag.upper(), color, supplier, tag_type, replace.upper())
        print query
        self.db.execute(query)
    
    def get_animals(self):
        return []
    
    def get_latest_samples(self):
        output = []
        try:
            self.db.execute('SELECT prefix, barcode, sample_time, comment FROM active_samples ORDER BY sample_time DESC;')
            for sample in self.db.fetchall():
                output.append(sample)
        except:
            output.append('Could not load latest samples')
        return output
    
    def update_samples(self, tag, info):
        match = self.prefixpattern.match(tag)
        prefix = match.group(0)
        barcode = tag[len(prefix):]
        try:
            self.db.execute('UPDATE samples SET comment = "%s" WHERE prefix = "%s" AND barcode = "%s";' % \
                (info[0][1], prefix, barcode))
        except:
            raise Exception('Could not update samples.')
        if info[1][1]:
            try:
                self.db.execute('INSERT INTO deleted_samples(prefix, barcode) VALUES ("%s", "%s");' % \
                    (prefix, barcode))
            except:
                raise Exception('Could not delete sample.')

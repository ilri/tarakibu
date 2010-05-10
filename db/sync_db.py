#!/usr/bin/env python

import MySQLdb
from datetime import datetime

external_db = {'user':'sampler',
               'pass':'5aMpL!n6+r1P',
               'host':'172.26.0.202',
               'db':'azizi'}

internal_db = {'user':'samples',
               'pass':'54mpl35',
               'host':'localhost',
               'db':'samples'}

exdb_conn = MySQLdb.connect(host  =external_db['host'],
                            user  =external_db['user'],
                            passwd=external_db['pass'],
                            db    =external_db['db'])

indb_conn = MySQLdb.connect(host  =internal_db['host'],
                            user  =internal_db['user'],
                            passwd=internal_db['pass'],
                            db    =internal_db['db'])
exdb = exdb_conn.cursor()
indb = indb_conn.cursor()

print '* Synchronizing databases'
print '* * Master: %s@%s' % (external_db['db'], external_db['host'])
print '* * Slave: %s@%s' % (internal_db['db'], internal_db['host'])

exdb.execute('SELECT a.animal_id, a.prev_tag, a.organism, a.approx_dob, a.sex, a.location, a.owner, c.observation_date, c.comments FROM custom_animals AS a JOIN custom_animal_comments AS c ON a.id = c.animal_id;')
for info in exdb.fetchall(): 
    animal_query = 'INSERT INTO animals (tag, date_of_birth, sex, owner) VALUES ("%s", "%s", "%s", "%s");' % (info[0], info[3], info[4], info[6])
    measure_query = 'INSERT INTO animal_measures (animal, sampling_date, comment) VALUES ("%s", "%s", "%s");' % (info[0], info[7], info[8])
    indb.execute(animal_query)
    indb.execute(measure_query)

print '* Finished'


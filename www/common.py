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

import re

class SimplePage():
    def __init__(self, settings, db, devices, info, logger):
        logger.info('Initializing the system settings')
        self.title = settings['name']
        self.version = settings['version']
        self.port = settings['port']
        self.radius = settings['radius']
        self.info_time = settings['info_time']
        self.db = db
        self.devices = devices
        self.info = info
        self.gps = devices['gps']


def gpsPosition(gps):
    """
    Return the current GPS position
    """
    if gps.status == 'initializing':
        return "<div class='gps_initializing'>Initializing</div>"
    if gps.status == 'Out of Sync':
        return "<div class='gps_out_of_sync'>Out of Sync</div>"
    if gps.status == 'running':
        return "<div class='gps_running'>%s, %s, %s, %s(%s)</div>" % (\
            gps_format(gps.data['latitude']), 
            gps_format(gps.data['longitude']), 
            gps.data['altitude'],
            gps.data['formattedTime'],
            gps.timeZoneName)
    return "<div class='gps_disconnected'>Disconnected</div>"


def gps_format(pos):
	"""
	Formats the raw longitude or latitude
	"""
	output = pos
	if type(pos) == type(float()):
		output = '%+.6f' % pos
		output = output.zfill(10)
	return output

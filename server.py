# SocialBearing Server Component
# Copyright (C) 2011-2012
#  * riot <riot@hackerfleet.org>
#  * cketti <cketti@c-base.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
import bottle
from bottle import route, run, request, abort
from pymongo import Connection
from bson.objectid import ObjectId

from voluptuous import Schema, required, all, range, match

connection = Connection('localhost', 27017)
db = connection.socialbearing

ver = "v1"

fullschema = Schema({
    required('device_uuid'): match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'),
    'device_model': unicode,
    required('buoys'): [
        {
            required('buoy_type'): unicode,
            'buoy_id': unicode,
            required('bearings'): [
                {
                    required('timestamp'): all(long, range(min=0)),
                    required('lat'): all(float, range(min=-180, max=180)),
                    required('lon'): all(float, range(min=-90, max=90)),
                    required('bearing'): all(int, range(min=0, max=359)),
                    required('accuracy'): all(float, range(min=0))
                }
            ]
        }
    ],
})

@route('/', method='GET')
def index():
    return """Versuchs mal mit nem POST von JSON Daten nach /%s/bearing oder 
    einem GET (mit bekannter buoy_id) nach /%s/bearing/$buoy_id ...
    """ % (ver, ver)

@route('/%s/bearing' %(ver), method='POST')
def post_bearing():
    data = request.body.readline()
    print data
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)

    # Validate input
    try:
        validated = fullschema(entity)
    except Exception, e:
        print e
        abort(400, "Invalid input data")

    try:
        db['bearings'].save(validated)
    except ValidationError as ve:
        abort(400, str(ve))

@route('/%s/bearing/:buoy_id' %(ver), method='GET')
def get_bearing(buoy_id):
    entity = db['bearings'].find_one({'_id': ObjectId(buoy_id)})
    if not entity:
        abort(404, 'No buoy with id %s' % buoy_id)
    return str(entity)

run(host='0.0.0.0', port=80, debug=True)

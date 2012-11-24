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

from voluptuous import Schema, required, all, length, range

connection = Connection('localhost', 27017)
db = connection.socialbearing

ver = "v1"

fullschema = Schema({
    required('device_uuid'): all(str, length(min=36, max=36)),
    'device_model': str,
    required('buoys'): [{}],
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

    #if not entity.has_key('_id'):
    #    abort(400, 'No _id specified')
    try:
        db['bearings'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

@route('/%s/bearing/:buoy_id' %(ver), method='GET')
def get_bearing(buoy_id):
    entity = db['bearings'].find_one({'_id': ObjectId(buoy_id)})
    if not entity:
        abort(404, 'No buoy with id %s' % buoy_id)
    return str(entity)

run(host='0.0.0.0', port=8080, debug=True)

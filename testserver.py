# EARLY VERSION for static testing! Do NOT use!

import json
import bottle
from bottle import route, run, request, abort
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.socialbearing

ver = "v1"

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
    entity = db['bearings'].find_one({'buoy_id': buoy_id})
    if not entity:
        abort(404, 'No buoy with id %s' % buoy_id)
    return entity

run(host='0.0.0.0', port=80)

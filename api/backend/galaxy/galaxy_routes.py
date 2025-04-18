from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

galaxy = Blueprint('galaxy', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#Get all item from Galaxies.
@galaxy.route('/galaxies', methods=['GET'])
def get_galaxy():
    query = '''
        SELECT * 
        FROM Galaxy
    '''
    run_program(query)


#Get specific info of a galaxy
@galaxy.route('/galaxies/<GalaxyID>', methods=['GET'])
def get_galaxy_detail (id):
    query = f'''
        SELECT * 
        FROM Galaxy
        WHERE GalaxyID = {str(id)}
    '''
    run_program(query)

#Put specific info into galaxies
@galaxy.route('/galaxies/<GalaxyID>', methods = ['PUT'])
def update_product():
    galaxy_info = request.json
    current_app.logger.info(galaxy_info)
    return "Success"

#--------------------------------------------------------------

#Get all star systems in a galaxy
@galaxy.route('/galaxies/<GalaxyID>/starsystems', methods=['GET'])
def get_starsystems (GID):
    query = f'''
        SELECT StarSystem.SystemName
        FROM StarSystem
        WHERE StarSystem.GalaxyID = str{(GID)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>', methods=['GET'])
def get_starsystem_info (GID, SID):
    query = f'''
        SELECT StarSystem.SystemName
        FROM StarSystem
        WHERE Galaxy.GalaxyID = str{(GID)} AND StarSystem.SystemID = str{(SID)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>', methods = ['PUT'])
def update_product():
    galaxy_info = request.json
    current_app.logger.info(galaxy_info)
    return "Success"

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<DistInLY>')
def get_starsystem_distInLY (GID, DLY):
    query = f'''
        SELECT StarSystem.SystemName
        FROM StarSystem
        WHERE StarSystem.GalaxyID = str{(GID)} AND StarSystem.DistInLY <= str{(DLY)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/numStars')
def get_starsystem_numStars (GID):
    query = f'''
        SELECT StarSystem.SystemName, StarSystem.NumStars
        FROM StarSystem
        WHERE StarSystem.GalaxyID = str{(GID)}
    '''
    run_program(query)

#-------------------------------------------------------------

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars')
def get_stars (GID, SID):
    query = f'''
        SELECT Star.StarName
        FROM Star
        WHERE Star.
    '''






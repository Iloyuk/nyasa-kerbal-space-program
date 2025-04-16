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


#Get all star systems in a galaxy
@galaxy.route('/starsystems')
def get_starsystems ():
    query = '''
        SELECT s.SystemName
        FROM Galaxy JOIN StarSystem s
        WHERE Galaxy.GalaxyID = s.GalaxyID
    '''
    run_program(query)






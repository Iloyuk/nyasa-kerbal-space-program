from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

star_system = Blueprint('star_system', __name__)

def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


# Get all star systems in a galaxy by galaxy id
@star_system.route('/galaxies/<int:GalaxyID>/starsystems', methods=['GET', 'POST', 'PUT'])
def find_starsystems_by_galaxy_id(GalaxyID):
    if request.method == 'GET':
        query = f'''
            SELECT SystemName
            FROM StarSystem
            WHERE GalaxyID = {GalaxyID}
        '''
        return run_program(query)

    elif request.method == 'POST':
        data = request.get_json()
        query = f'''
            INSERT INTO StarSystem (GalaxyID, SystemName, DistInLY, SystemType, NumStars)
            VALUES ({GalaxyID}, '{data['SystemName']}', {data['DistInLY']}, '{data['SystemType']}', {data['NumStars']})
            '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query)
            db.get_db().commit()
            return jsonify({'message': 'Star System inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        query = f'''
            UPDATE StarSystem
            SET GalaxyID = {GalaxyID},
                SystemName = {data['SystemName']},
                DistInLY = {data['DistInLY']},
                SystemType = '{data['SystemType']}',
                NumStars = {data['NumStars']}
            WHERE SystemID = '{data['SystemID']}'
            '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query)
            db.get_db().commit()
            return jsonify({
                'message': 'Star system updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Get all star systems in a galaxy by galaxy name
@star_system.route('/galaxies/<GalaxyName>/starsystems', methods=['GET'])
def find_starsystems_by_galaxy_name(GalaxyName):
    query = f'''
        SELECT S.SystemName
        FROM StarSystem S JOIN Galaxy G on S.GalaxyID = G.GalaxyID
        WHERE G.GalaxyName LIKE '%{GalaxyName}%'
        '''
    return run_program(query)


# Get a star system by its id
@star_system.route('/galaxies/starsystems/<int:SystemID>', methods=['GET'])
def find_starsystems_by_starsystem_name(SystemID):
    query = f'''
        SELECT *
        FROM StarSystem
        WHERE SystemID = {SystemID}
    '''
    return run_program(query)


# Get a star system by a combination of galaxy name and star system name
@star_system.route('/galaxies/<GalaxyName>/starsystems/<SystemName>', methods=['GET'])
def find_starsystems_by_galaxy_name_and_starsystem_name(GalaxyName, SystemName):
    query = f'''
        SELECT *
        FROM StarSystem SS JOIN Galaxy G on SS.GalaxyID = G.GalaxyID
        WHERE G.GalaxyName LIKE '%{GalaxyName}%' AND SS.SystemName LIKE '%{SystemName}%'
    '''
    return run_program(query)
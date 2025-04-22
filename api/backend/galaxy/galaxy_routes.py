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
    db.get_db().commit()
    return response

# -------------------------------------------------------------- Galaxies

# Do stuff with galaxies
@galaxy.route('/galaxies', methods=['GET', 'POST', 'PUT'])
def get_galaxies():
    if request.method == 'GET':
        query = '''
            SELECT * 
            FROM Galaxy
            LIMIT 10
        '''
        return run_program(query)

    elif request.method == 'POST':
        data = request.get_json()
        query = '''
            INSERT INTO Galaxy (GalaxyName, Redshift, YearDiscovered, SolarMassTrillions, DominantElement)
            VALUES (%s, %s, %s, %s, %s)
            '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                data['GalaxyName'],
                float(data['Redshift']),
                data['YearDiscovered'],
                int(data['SolarMassTrillions']),
                data['DominantElement']
            ))
            db.get_db().commit()
            return jsonify({'message': 'Galaxy inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        query = '''
            UPDATE Galaxy
            SET GalaxyName = %s,
                Redshift = %s,
                YearDiscovered = %s,
                SolarMassTrillions = %s,
                DominantElement = %s
            WHERE GalaxyID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                data['GalaxyName'],
                float(data['Redshift']),
                data['YearDiscovered'],
                int(data['SolarMassTrillions']),
                data['DominantElement'],
                data['GalaxyID']
            ))
            db.get_db().commit()
            return jsonify({
                'message': 'Galaxy updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Get names of galaxies
@galaxy.route('/galaxies/names', methods=['GET'])
def get_galaxy_names():
    query = '''
        SELECT GalaxyName
        FROM Galaxy
        LIMIT 10
        '''
    return run_program(query)


# Get specific info of a galaxy from galaxy name
@galaxy.route('/galaxies/<GalaxyName>', methods=['GET'])
def find_galaxy_by_name(GalaxyName):
    query = f'''
        SELECT *
        FROM Galaxy
        WHERE GalaxyName LIKE '%{GalaxyName}%'
        '''
    return run_program(query)


# Get specific info of a galaxy from galaxy ID
@galaxy.route('/galaxies/<int:GalaxyID>', methods=['GET'])
def find_galaxy_by_id(GalaxyID):
    query = f'''
        SELECT * 
        FROM Galaxy
        WHERE GalaxyID = {GalaxyID}
    '''
    return run_program(query)


# -------------------------------------------------------------- Star Systems

# Get all star systems in a galaxy by galaxy id
@galaxy.route('/galaxies/<int:GalaxyID>/starsystems', methods=['GET', 'POST', 'PUT'])
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
@galaxy.route('/galaxies/<GalaxyName>/starsystems', methods=['GET'])
def find_starsystems_by_galaxy_name(GalaxyName):
    query = f'''
        SELECT S.SystemName
        FROM StarSystem S JOIN Galaxy G on S.GalaxyID = G.GalaxyID
        WHERE G.GalaxyName LIKE '%{GalaxyName}%'
        '''
    return run_program(query)


# Get a star system by its id
@galaxy.route('/galaxies/starsystems/<int:SystemID>', methods=['GET'])
def find_starsystems_by_starsystem_name(SystemID):
    query = f'''
        SELECT *
        FROM StarSystem
        WHERE SystemID = {SystemID}
    '''
    return run_program(query)


# Get a star system by a combination of galaxy name and star system name
@galaxy.route('/galaxies/<GalaxyName>/starsystems/<SystemName>', methods=['GET'])
def find_starsystems_by_galaxy_name_and_starsystem_name(GalaxyName, SystemName):
    query = f'''
        SELECT *
        FROM StarSystem SS JOIN Galaxy G on SS.GalaxyID = G.GalaxyID
        WHERE G.GalaxyName LIKE '%{GalaxyName}%' AND SS.SystemName LIKE '%{SystemName}%'
    '''
    return run_program(query)


# -------------------------------------------------------------- Stars

# Add or update stars
@galaxy.route('/stars', methods=['POST', 'PUT'])
def add_or_update_stars():
    if request.method == 'POST':
        data = request.get_json()
        query = '''
            INSERT INTO Star (SystemID, ConstID, StarName, Mass, Temperature, SpectralType) 
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                int(data['SystemID']),
                int(data['ConstID']),
                data['StarName'],
                int(data['Mass']),
                int(data['Temperature']),
                data['SpectralType']
            ))
            db.get_db().commit()
            return jsonify({'message': 'Star System inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        query = '''
            UPDATE Star
            SET SystemID = %s,
                ConstID = %s,
                StarName = %s,
                Mass = %s,
                Temperature = %s,
                SpectralType = %s
            WHERE StarID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                int(data['SystemID']),
                int(data['ConstID']),
                data['StarName'],
                int(data['Mass']),
                int(data['Temperature']),
                data['SpectralType'],
                int(data['StarID'])
            ))
            db.get_db().commit()
            return jsonify({
                'message': 'Star updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Find star based on star system name
@galaxy.route('/star_systems/<SystemName>', methods=['GET'])
def get_stars_by_system_name(SystemName):
    query = f'''
        SELECT StarName, StarID
        FROM Star S JOIN StarSystem SS ON S.SystemID = SS.SystemID
        WHERE SS.SystemName LIKE '%{SystemName}%'
    '''
    return run_program(query)


# Find star based on star system id
@galaxy.route('/star_systems/<int:SystemID>', methods=['GET'])
def get_stars_by_system_id(SystemID):
    query = f'''
        SELECT StarName, StarID
        FROM Star
        WHERE SystemID = {SystemID}
    '''
    return run_program(query)


# Get info on a specific star
@galaxy.route('/stars/<StarID>', methods=['GET'])
def get_star_info(StarID):
    query = f'''
        SELECT *
        FROM Star
        WHERE StarID = {StarID}
    '''
    return run_program(query)


# -------------------------------------------------------------- Planets

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets', methods=['GET'])
def get_planet(GalaxyID, SystemID, StarID):
    query = f'''
        SELECT Planet.PlanetName
        FROM Orbits JOIN Planet
        WHERE Orbits.StarID = {StarID} 
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['GET'])
def get_planet_info(GalaxyID, SystemID, StarID, PlanetID):
    query = f'''
        SELECT Planet.PlanetName
        FROM Planet
        WHERE Planet.PlanetID = {(PlanetID)}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['PUT'])
def update_planet(GalaxyID, SystemID, StarID, PlanetID):
    planet_info = request.json
    current_app.logger.info(planet_info)
    return "Success"


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['POST'])
def add_planet(GalaxyID, SystemID, StarID, PlanetID):
    planet_info = request.json

    planetID = {(PlanetID)}
    planetName = planet_info['PlanetName']
    planetType = planet_info['PlanetType']
    mass = planet_info['Mass']
    numMoons = planet_info['NumMoons']
    eccentricity = planet_info['Eccentricity']
    inclination = planet_info['Inclination']
    query = f'''
        INSERT INTO Planet (PlanetID, PlanetName, PlanetType, Mass, NumMoons, Eccentricity, Inclination)
        VALUES (str{planetID}, {planetName}, {planetType}, str{mass}, str{numMoons}, str{eccentricity}, str{inclination})
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['DELETE'])
def delete_planet(GalaxyID, SystemID, StarID, PlanetID):
    query = f'''
        DELETE FROM Planet
        WHERE Planet.PlanetID = str{PlanetID}
    '''
    return run_program(query)

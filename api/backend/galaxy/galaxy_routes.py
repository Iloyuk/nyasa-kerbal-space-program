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


@galaxy.route('/')
def welcome():
    current_app.logger.info('GET / handler')
    welcome_message = '<h1>Welcome to the CS 3200 Project Template REST API'
    response = make_response(welcome_message)
    response.status_code = 200
    return response


# Get all galaxies, with a limit of 10
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
            return jsonify({'message': 'Star inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        query = '''
            UPDATE Galaxy
            SET Redshift = %s,
                YearDiscovered = %s,
                SolarMassTrillions = %s,
                DominantElement = %s
            WHERE GalaxyName = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                float(data['Redshift']),
                data['YearDiscovered'],
                int(data['SolarMassTrillions']),
                data['DominantElement'],
                data['GalaxyName']
            ))
            db.get_db().commit()
            return jsonify({
                'message': 'Galaxy updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Get specific info of a galaxy from galaxy name
@galaxy.route('/galaxies/<GalaxyName>', methods=['GET'])
def find_galaxy(GalaxyName):
    query = f'''
        SELECT *
        FROM Galaxy
        WHERE GalaxyName LIKE '%{GalaxyName}%'
        '''
    return run_program(query)


# Get specific info of a galaxy from galaxy id
@galaxy.route('/galaxies/<int:GalaxyID>', methods=['GET'])
def get_galaxy_detail_int(GalaxyID):
    query = f'''
        SELECT * 
        FROM Galaxy
        WHERE GalaxyID = {GalaxyID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/elements/<DominantElement>', methods=['GET'])
def get_galaxy_domElement(DominantElement):
    query = f'''
        SELECT GalaxyName
        FROM Galaxy
        WHERE DominantElement = {DominantElement};
    '''
    return run_program(query)


# --------------------------------------------------------------

# Get all star systems in a galaxy
@galaxy.route('/galaxies/<GalaxyID>/starsystems', methods=['GET'])
def get_starsystems(GalaxyID):
    query = f'''
        SELECT StarSystem.SystemName
        FROM StarSystem
        WHERE StarSystem.GalaxyID = {GalaxyID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>', methods=['GET'])
def get_starsystem_info(GalaxyID, SystemID):
    query = f'''
        SELECT *
        FROM StarSystem
        WHERE StarSystem.SystemID = {SystemID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>', methods=['PUT'])
def update_system():
    system_info = request.json
    current_app.logger.info(system_info)
    return "Success"


@galaxy.route('/galaxies/<GalaxyID>/starsystems/DistInLY', methods=['GET'])
def get_all_starsystem_distInLY(GalaxyID):
    query = f'''
        SELECT StarSystem.SystemName, StarSystem.DistInLY
        FROM StarSystem
        WHERE StarSystem.GalaxyID = {GalaxyID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/DistInLY/<DistInLY>', methods=['GET'])
def get_starsystem_distInLY(GalaxyID, DistInLY):
    query = f'''
        SELECT StarSystem.SystemName, StarSystem.DistInLY
        FROM StarSystem
        WHERE StarSystem.GalaxyID = {GalaxyID} AND StarSystem.DistInLY <= {DistInLY}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/numStars', methods=['GET'])
def get_starsystem_numStars(GalaxyID):
    query = f'''
        SELECT StarSystem.SystemName, StarSystem.NumStars
        FROM StarSystem
        WHERE StarSystem.GalaxyID = {GalaxyID}
    '''
    return run_program(query)


# -------------------------------------------------------------

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars', methods=['GET'])
def get_stars(GalaxyID, SystemID):
    query = f'''
        SELECT *
        FROM Star
        WHERE Star.SystemID = {SystemID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>', methods=['GET'])
def get_stars_info(GalaxyID, SystemID, StarID):
    query = f'''
        SELECT *
        FROM Star
        WHERE Star.StarID = {StarID} AND Star.SystemID = {SystemID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>', methods=['PUT'])
def update_star(GalaxyID, SystemID, StarID):
    star_info = request.json
    current_app.logger.info(star_info)
    return "Success"


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>', methods=['POST'])
def add_star(GalaxyID, SystemID, StarID):
    star_info = request.json

    starID = star_info['StarID']
    systemID = star_info['SystemID']
    constID = star_info['ConstID']
    starName = star_info['StarName']
    mass = star_info['Mass']
    temperature = star_info['Temperature']
    spectralType = star_info['SpectralType']

    query = f'''
        INSERT INTO Star (StarID, SystemID, ConstID, StarName, Mass, Temperature, SpectralType)
        VALUES ({starID}, {systemID}, {constID}, {starName}, {mass}, {temperature}, {spectralType})
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/Mass', methods=['GET'])
def get_star_mass(GalaxyID, SystemID):
    query = f'''
    SELECT StarName, Mass
    FROM Star
    WHERE Star.SystemID = {SystemID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/Mass/<Mass>', methods=['GET'])
def search_star_from_mass(GalaxyID, SystemID, Mass):
    query = f'''
    SELECT Star.StarName, Star.Mass
    FROM Star
    WHERE Mass < {Mass} AND Star.SystemID = {SystemID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/temperature', methods=['GET'])
def get_star_temp(GalaxyID, SystemID):
    query = f'''
    SELECT Star.StarName, Star.Temperature
    FROM Star
    WHERE Star.SystemID = {SystemID}
    '''
    return run_program(query)


@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/temperature/<Temperature>', methods=['GET'])
def search_star_from_temperature(GalaxyID, SystemID, Temperature):
    query = f'''
    SELECT Star.StarName, Star.Temperature
    FROM Star
    WHERE Temperature < {Temperature} AND Star.SystemID = {SystemID}
    '''
    return run_program(query)


#---------------------------------------------------------------------------------

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

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
def update_galaxy():
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
def update_system():
    system_info = request.json
    current_app.logger.info(system_info)
    return "Success"

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<DistInLY>', methods=['GET'])
def get_starsystem_distInLY (GID, DLY):
    query = f'''
        SELECT StarSystem.SystemName
        FROM StarSystem
        WHERE StarSystem.GalaxyID = str{(GID)} AND StarSystem.DistInLY <= str{(DLY)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/numStars', methods=['GET'])
def get_starsystem_numStars (GID):
    query = f'''
        SELECT StarSystem.SystemName, StarSystem.NumStars
        FROM StarSystem
        WHERE StarSystem.GalaxyID = str{(GID)}
    '''
    run_program(query)

#-------------------------------------------------------------

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars', methods=['GET'])
def get_stars (SID):
    query = f'''
        SELECT *
        FROM Star
        WHERE Star.SystemID = str{(SID)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>', methods=['GET'])
def get_stars_info (SID):
    query = f'''
        SELECT *
        FROM Star
        WHERE Star.StarID = str{(SID)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>', methods = ['PUT'])
def update_star():
    star_info = request.json
    current_app.logger.info(star_info)
    return "Success"

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>', methods = ['POST'])
def add_star():
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
        VALUES (str{(starID)}, str{(systemID)}, str{(constID)}, {starName}, str{(mass)}, str{(temperature)}, {spectralType})
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<Mass>', methods=['GET'])
def search_star_from_mass(mass):
    query = f'''
    SELECT StarName, Mass
    FROM Star
    WHERE Mass < str{(mass)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<Temperature>', methods=['GET'])
def search_star_from_temperature(temp):
    query = f'''
    SELECT StarName, Temperature
    FROM Star
    WHERE Mass < str{(temp)}
    '''
    run_program(query)

#---------------------------------------------------------------------------------

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets', methods=['GET'])
def get_planet (SID):
    query = f'''
        SELECT Planets.PlanetName
        FROM Orbits JOIN Planets
        WHERE Orbits.StarID = str{(SID)} 
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['GET'])
def get_planet_info (PID):
    query = f'''
        SELECT Planets.PlanetName
        FROM Planets
        WHERE Planet.PlanetID = str{(PID)}
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['PUT'])
def update_planet ():
    planet_info = request.json
    current_app.logger.info(planet_info)
    return "Success"

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['POST'])
def add_planet ():
    planet_info = request.json

    planetID = planet_info['PlanetID']
    planetName = planet_info['PlanetName']
    planetType = planet_info['PlanetType'] 
    mass = planet_info['Mass'] 
    numMoons = planet_info['NumMoons']
    eccentricity = planet_info['Eccentricity'] 
    inclination = planet_info['Inclination']
    query = f'''
        INSERT INTO Planet (PlanetID, PlanetName, PlanetType, Mass, NumMoons, Eccentricity, Inclination)
        VALUES (str{(planetID)}, {planetName}, {planetType}, str{(mass)}, str{(numMoons)}, str{(eccentricity)}, str{(inclination)})
    '''
    run_program(query)

@galaxy.route('/galaxies/<GalaxyID>/starsystems/<SystemID>/stars/<StarID>/planets/<PlanetID>', methods=['DELETE'])
def delete_planet (PID):
    query = f'''
        DELETE FROM Planet
        WHERE Planet.PlanetID = str{(PID)}
    '''
    run_program(query)









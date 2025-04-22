from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

planet = Blueprint('planet', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


@planet.route('/planet/orbits', methods=['GET'])
def get_planets_that_orbit_star():
    star_identifier = request.args.get('star')
    cursor = db.get_db().cursor()

    if star_identifier.isnumeric():
        query = '''
                SELECT S.StarName AS 'MainStar', P.PlanetID, P.PlanetName, O.OrbitalPeriod, O.SemiMajorAxis
                FROM Star S JOIN Orbits O on S.StarID = O.StarID
                            JOIN Planet P on O.PlanetID = P.PlanetID
                WHERE S.StarID = %s
            '''
        cursor.execute(query, star_identifier)
    else:
        query = '''
                SELECT S.StarName AS 'MainStar', P.PlanetID, P.PlanetName, O.OrbitalPeriod, O.SemiMajorAxis
                FROM Star S JOIN Orbits O on S.StarID = O.StarID
                            JOIN Planet P on O.PlanetID = P.PlanetID
                WHERE S.StarName LIKE %s
            '''
        cursor.execute(query, (f"%{star_identifier}%",))

    try:
        theData = cursor.fetchall()
        response = make_response(jsonify(theData))
        response.status_code = 200
        db.get_db().commit()
        return response
    except Exception as e:
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 400


@planet.route('/planet/<int:PlanetID>', methods=['GET'])
def get_planets_by_id(PlanetID):
    query = f'''
        SELECT *
        FROM Planet
        WHERE PlanetID = {PlanetID}
    '''
    return run_program(query)


@planet.route('/planet/<PlanetName>', methods=['GET'])
def get_planets_by_name(PlanetName):
    query = f'''
        SELECT *
        FROM Planet
        WHERE PlanetName LIKE '%{PlanetName}%'
    '''
    return run_program(query)
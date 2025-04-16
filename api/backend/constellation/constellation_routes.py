from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from enum import Enum

constellation = Blueprint('constellation', __name__)

class Hemisphere(Enum):
    North = 1
    South = 2

def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@constellation.route('/constellation', methods=['GET'])
def get_constellation():
    query = '''
        SELECT * 
        FROM Constellation
    '''
    run_program(query)

@constellation.route('/constellation/<ConstID>', methods=['GET'])
def get_constellation_info(id):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.ConstID = str{(id)}
    '''
    run_program(query)

@constellation.route('/constellation/brightestStar', methods=['GET'])
def get_brightest_star():
    query = f'''
        SELECT C.ConstName, S.StarName
        FROM Constellation C JOIN Star S ON C.BrightestStar = S.StarName;
    '''
    run_program(query)

@constellation.route('/constellation/<bestViewingMonth>', method=['GET'])
def get_const_best_view(month):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.BestViewingMonth = str{(month)}
    '''
    run_program(query)

@constellation.route('/constellation/<hemisphere>', method=['GET'])
def get_const_hemisphere(hemisphere):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.hemisphere = str{(hemisphere)}
    '''
    run_program(query)

@constellation.route('/constellation/<ConstName>', method=['GET'])
def get_const_by_name(name):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.ConstName= str{(name)}
    '''
    run_program(query)






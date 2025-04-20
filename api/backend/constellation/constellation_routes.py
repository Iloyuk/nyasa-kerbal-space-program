from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from enum import Enum

constellation = Blueprint('constellation', __name__)

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
    return run_program(query)

@constellation.route('/constellation/<ConstID>', methods=['GET'])
def get_constellation_info(ConstID):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.ConstID = str{(ConstID)}
    '''
    return run_program(query)

@constellation.route('/constellation/brightestStar', methods=['GET'])
def get_brightest_star():
    query = f'''
        SELECT C.ConstName, S.StarName
        FROM Constellation C JOIN Star S ON C.BrightestStar = S.StarName;
    '''
    return run_program(query)


@constellation.route('/constellation/bestViewingMonth', method=['GET'])
def find_const_best_view():
    query = f'''
        SELECT Constellation.BestViewingMonth
        FROM Constellation
    '''
    return run_program(query)

@constellation.route('/constellation/bestViewingMonth/<bestViewingMonth>', method=['GET'])
def get_const_best_view(bestViewingMonth):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.BestViewingMonth = {(bestViewingMonth)}
    '''
    return run_program(query)

@constellation.route('/constellation/hemisphere', method=['GET'])
def find_const_hemisphere():
    query = f'''
        SELECT Constellation.Hemisphere 
        FROM Constellation
    '''
    run_program(query)

@constellation.route('/constellation/hemisphere/<Hemisphere>', method=['GET'])
def get_const_hemisphere(Hemisphere):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.Hemisphere = {(Hemisphere)}
    '''
    run_program(query)

@constellation.route('/constellation/name/<ConstName>', method=['GET'])
def get_const_by_name(ConstName):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.ConstName= {(ConstName)}
    '''
    run_program(query)






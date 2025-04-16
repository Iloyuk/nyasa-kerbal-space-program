from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

astronauts = Blueprint('astronauts', __name__)

def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@astronauts.route('/astronauts', methods=['GET'])
def get_astronaut():
    query = '''
        SELECT * 
        FROM Astronaut
    '''
    run_program(query)

@astronauts.route('/astronauts/<AstroID>', methods=['GET'])
def get_astronaut_info(id):
    query = f'''
        SELECT * 
        FROM Astronaut
        WHERE Astronaut.AstroID = str{(id)}
    '''
    run_program(query)

@astronauts.route('/astronauts/onMission', methods=['GET'])
def get_astronaut_on_mission():
    query = '''
        SELECT A.Name, M.MissionName, M.Objective
        FROM Astronaut A
        JOIN MissionAstronaut MA on A.AstroID = MA.AstroID
        JOIN Mission M on MA.MissionID = M.MissionID
        JOIN StarSystemMissions SSM on MA.MissionID = SSM.MissionID
        WHERE SSM.EndDate IS NULL;
    '''
    run_program(query)


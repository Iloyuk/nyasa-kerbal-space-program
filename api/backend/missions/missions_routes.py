from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

mission = Blueprint('mission', __name__)

def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@mission.route('/missions', methods=['GET'])
def get_mission():
    query = '''
        SELECT * FROM Mission NATURAL JOIN StarSystemMissions;
    '''
    return run_program(query)

@mission.route('/missions/<MissionID>', methods=['GET'])
def get_mission_info(MissionID):
    query = f'''
        SELECT * 
        FROM Mission
        WHERE Mission.MissionID = {(MissionID)}
    '''
    return run_program(query)

@mission.route('/missions/<MissionID>', methods=['PUT'])
def change_mission_status(MissionID):
    query = f'''
    UPDATE StarSystemMissions
    SET EndDate = now()
    WHERE StarSystemMissions.MissionID = {MissionID};

    '''
    return run_program(query)

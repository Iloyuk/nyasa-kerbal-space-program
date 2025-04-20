from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

findings = Blueprint('findings', __name__)

def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


@findings.route('/findings', methods=['GET'])
def get_finding():
    query = '''
        SELECT * 
        FROM Finding
    '''
    return run_program(query)

@findings.route('/findings/<FindingID>', methods=['GET'])
def get_finding (FindingID):
    query = f'''
        SELECT * 
        FROM Finding
        WHERE FindingID = {(FindingID)}
    '''
    return run_program(query)

@findings.route('/findings/significance', methods=['GET'])
def finding_high_sig ():
    query = f'''
        SELECT M.MissionName, M.Objective, F.FindingDate, F.Notes
        FROM Mission M
            JOIN MissionFinding MF ON M.MissionID = MF.MissionID
            JOIN Finding F ON MF.FindingID = F.FindingID
        '''
    return run_program(query)

@findings.route('/findings/significance/<Significance>', methods=['GET'])
def get_finding_high_sig (sig):
    query = f'''
        SELECT M.MissionName, M.Objective, F.FindingDate, F.Notes
        FROM Mission M
            JOIN MissionFinding MF ON M.MissionID = MF.MissionID
            JOIN Finding F ON MF.FindingID = F.FindingID
        WHERE F.Significance = str{(sig)}
        '''
    return run_program(query)
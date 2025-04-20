from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from enum import Enum

mission = Blueprint('mission', __name__)

def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@mission.route('/missions', methods=['GET'])
def get_spacecraft():
    query = '''
        SELECT * 
        FROM Mission
    '''
    return run_program(query)


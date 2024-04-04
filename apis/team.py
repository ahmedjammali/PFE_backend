from flask import Blueprint, jsonify , request
from config import get_connection
from datetime import timedelta

team_blueprint = Blueprint('team_api', __name__)

conn = get_connection()
cursor = conn.cursor()


@team_blueprint.route('/check_team_leader', methods=['POST'])
def check_team_leader():
    user_role = request.json.get('user_role')
    team_id =request.json.get('team_id')

    if user_role is None or team_id is None:
        return jsonify({'error': 'User ID not provided'}), 400

    

    if user_role == 3:
        cursor.execute("SELECT * FROM TriSQR_Team WHERE Id = ?", (team_id,))
        team_leader = cursor.fetchone()
        team_id = team_leader[0]
        team_name = team_leader[1]
        cursor.execute("SELECT Users_name , Users_Last_Name , Users_Login , privilege_id, Id FROM TriSQR_Users WHERE Team = ? and IsActive = 1", (team_id,))
        members = cursor.fetchall()
        response = {
            'team_leader': True,
            'team_name': team_name,
            'team_members': [{'user_name': member[0], 'last_name': member[1], 'email': member[2], 'privilege': member[3], 'Id': member[4], 'real_team_leader': True if member[4] in [row[0] for row in cursor.execute("SELECT Team_Leader FROM TriSQR_Team where Team_Leader = ?", (member[4],))] else False} for member in members]
        }
        return jsonify(response)
    else:
        return jsonify({'team_leader': False})

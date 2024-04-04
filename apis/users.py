from flask import Blueprint, jsonify , request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from config import get_connection
from datetime import timedelta

user_blueprint = Blueprint('user_api', __name__)


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json  
    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM TriSQR_Users WHERE Users_Login = ? AND Users_Password = ? and IsActive = 1 and Users_Role in (1,2,4)"
    cursor.execute(query, (email, password))

    user = cursor.fetchone()

    if user:
        user_data = {
            'user_id': user[0],
            'username': user[1],
            'user_last_name' : user[2],
            'user_Login' : user[3],
            'user_role' : user[5],
            'user_team' : user[18],
            'user_prev' : user[19]
        }
        access_token = create_access_token(identity=user_data)

        return jsonify({'message':'Login successful','user': user_data, 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 400

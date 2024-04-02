from flask import Blueprint, jsonify , request
from config import get_connection

privilege_blueprint = Blueprint('privilege_api', __name__)

conn = get_connection()
cursor = conn.cursor()


@privilege_blueprint.route('/modify_privilege', methods=['POST'])
def modify_privilege():
    data = request.json
    user_name = data.get('user_name')
    user_last_name = data.get('user_last_name')
    user_role = data.get('user_role')

    print(user_name , user_last_name, user_role)

    query = "SELECT * FROM TriSQR_Users WHERE Users_Name = ? AND Users_Last_Name = ?"
    cursor.execute(query, (user_name, user_last_name))

    user = cursor.fetchone()

    if user:
        # Update privilege based on user role
        privilege = 0
        if user_role == 'read':
            privilege = 1
        elif user_role == 'write':
            privilege = 2
        elif user_role == 'TL':
            privilege = 3

        print(privilege)
        update_query = "UPDATE TriSQR_Users SET privilege_id = ? WHERE Users_Name = ? AND Users_Last_Name = ?"
        cursor.execute(update_query, (privilege, user_name, user_last_name))
        conn.commit()
        return jsonify({'message': 'Privilege updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404



from flask import Blueprint, jsonify , request
from config import get_connection


Folder_blueprint = Blueprint('Folder_api', __name__)

conn = get_connection()
cursor = conn.cursor()
@Folder_blueprint.route('/get_folder_numbers', methods=['POST'])
def get_folder():
    user_Id = request.json.get('user_id')

    if user_Id is None:
        return jsonify({'error': 'User ID not provided'}), 400

    try:
        folder_counts = {}

        cursor.execute("SELECT COUNT(*) FROM TriSQR_Folder WHERE affectation = ? AND positionRefId = 1", (user_Id,))
        folder_counts['positionRefId_1'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM TriSQR_Folder WHERE affectation = ? AND positionRefId = 3",(user_Id,))
        folder_counts['positionRefId_3'] = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM TriSQR_Folder WHERE affectation =? AND positionRefId = 4", (user_Id,))
        folder_counts['positionRefId_4'] = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM TriSQR_Folder WHERE affectation = ? AND positionRefId = 5", (user_Id,))
        folder_counts['positionRefId_5'] = cursor.fetchone()[0]

        return jsonify(folder_counts), 200

    except Exception as e:

        return jsonify({'error': str(e)}), 500
    
@Folder_blueprint.route('/get_folder_data', methods=['POST'])
def get_ftp_folder():
    user_Id = request.json.get('user_id')
    folder_position = request.json.get('folder_position')

    if user_Id is None or folder_position is None:
        return jsonify({'error': 'User ID or folder position is not provided'}), 400
    
    try:
        cursor.execute("SELECT Id, code_client, raison_sociale, nYear, date_livraison FROM TriSQR_Folder WHERE affectation = ? AND positionRefId = ?", (user_Id, folder_position))
        folders = cursor.fetchall()
        
        response = {
            'folders': [{'Id': folder[0], 'code_client': folder[1], 'raison_sociale': folder[2], 'nYear': folder[3], 'date_livraison': folder[4]} for folder in folders]
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
    


from flask import Blueprint, jsonify, request
from config import get_connection

Files_blueprint = Blueprint('Files_api', __name__)

@Files_blueprint.route('/add_files', methods=['POST'])
def add_files():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        file_title = data.get('file_title')
        file_description = data.get('file_description')
        file_link = data.get('file_link')
        file_date = data.get('file_date')
        folder_Id = data.get('folder_Id')



        if None in (file_title, file_description, file_link, file_date, folder_Id):
            return jsonify({'error': 'there is missing data'}), 400

        query = "INSERT INTO TriSQR_files (title, description, Link, date, folder_id) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (file_title, file_description, file_link, file_date, folder_Id))
        conn.commit()
        return jsonify({'success': 'file added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()



@Files_blueprint.route('/get_files', methods=['POST'])
def get_files():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        folder_Id = data.get('folder_Id')

        if folder_Id is None:
            return jsonify({'error': 'folder_Id is missing'}), 400


        query = "select * from TriSQR_files where folder_id = ? "
        cursor.execute(query, (folder_Id))
        files = cursor.fetchall()
        
        file_list = []
        for file_data in files:
            file_dict = {
                'fileId': file_data[0],
                'file_title': file_data[1],
                'description': file_data[2],
                'Link': file_data[3],
                'date': file_data[4]
            }
            file_list.append(file_dict)

        return jsonify(file_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@Files_blueprint.route('/delete_file', methods=['POST'])
def delete_file():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        file_id = data.get('file_id')

        if file_id is None:
            return jsonify({'error': 'there is missing data'}), 400

        query = "DELETE FROM TriSQR_files WHERE id = ?;"
        cursor.execute(query, (file_id))
        conn.commit()
        return jsonify({'success': 'file delete successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

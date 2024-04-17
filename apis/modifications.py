from flask import Blueprint, jsonify , request
from config import get_connection


modfication_blueprint = Blueprint('modification_api', __name__)

conn = get_connection()
cursor = conn.cursor()
@modfication_blueprint.route('/add_modification', methods=['POST'])
def add_modifcation():
    
    try : 
        data = request.json
        table_name = data.get('TN')
        table_header = data.get('TH')
        date = data.get('date')
        beforeM = data.get('beforeM')
        afterM = data.get('afterM')
        file_id = data.get('file_id')

        if None in (table_name,table_header,date , beforeM , afterM , file_id):
                return jsonify({'error': 'there is missing data'}), 400
        
        query = "INSERT INTO TriSQR_modifications (table_name , header,modification_date,before_modification , after_modification , file_id) VALUES (?, ?, ?, ?, ? , ?)"

        cursor.execute(query, (table_name, table_header, date, beforeM,afterM, file_id))
        conn.commit()
        return jsonify({'success': 'modification added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@modfication_blueprint.route('/get_modification', methods=['POST'])
def get_modification():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        file_Id = data.get('file_Id')

        if file_Id is None:
            return jsonify({'error': 'file_id is missing'}), 400


        query = "select * from TriSQR_modifications where file_id = ? "
        cursor.execute(query, (file_Id))
        files = cursor.fetchall()
        
        file_list = []
        for file_data in files:
            file_dict = {
                'ID' : file_data[0],
                'TN': file_data[1],
                'TH': file_data[2],
                'date': file_data[3],
                'beforM': file_data[4],
                'afterM': file_data[5]
            }
            file_list.append(file_dict)

        return jsonify(file_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

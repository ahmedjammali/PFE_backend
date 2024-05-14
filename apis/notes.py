from flask import Blueprint, jsonify , request
from config import get_connection


note_blueprint = Blueprint('note_api', __name__)

conn = get_connection()
cursor = conn.cursor()
@note_blueprint.route('/add_note', methods=['POST'])
def add_note():

    try :
        data = request.json
        task_id = data.get('task_id')
        note_text = data.get('note_text')
        date = data.get('date')
        writed_by  =data.get('writed_by')

        

        if task_id is None or note_text is None or date is None or writed_by is None :
            return jsonify({'error': 'One or more variables are empty'}), 400

        sql_query = "INSERT INTO notes (task_id, note_text, created_date, writed_by) VALUES (?, ?, ?, ?)"
    
        cursor.execute(sql_query, (task_id, note_text, date, writed_by))

        conn.commit()


        return jsonify({'success': 'note inserted successfully'}), 200
    
    except Exception as e:

        return jsonify({'error': str(e)}), 500

@note_blueprint.route('/get_notes_by_task', methods=['POST'])
def get_notes_by_task():

    try :
        data = request.json
        task_id = data.get('task_id')

        

        if  task_id is None :
            return jsonify({'error': ' variable is empty'}), 400

        sql_query = "select * from notes where task_id = ?"
    
        cursor.execute(sql_query, ( task_id))

        notes = cursor.fetchall()
        
        note_list = []
        for note_data in notes:
            note_dict = {
                'noteId': note_data[0],
                'task_id': note_data[1],
                'note_text': note_data[2],
                'date': note_data[3],
                'writed_by': note_data[4],
            }
            note_list.append(note_dict)

        return jsonify(note_list)

    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
    

@note_blueprint.route('/delete_task_notes', methods=['POST'])
def delete_task_notes():

    try :
        data = request.json
        task_id = data.get('task_id')

        

        if  task_id is None :
            return jsonify({'error': ' variable is empty'}), 400



        query = "delete from notes where task_id = ? "
        cursor.execute(query, (task_id))
        conn.commit()

        return jsonify({"message" : "notes deleted"}) , 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
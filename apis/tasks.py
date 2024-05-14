from flask import Blueprint, jsonify , request
from config import get_connection


task_blueprint = Blueprint('task_api', __name__)

conn = get_connection()
cursor = conn.cursor()
@task_blueprint.route('/add_task', methods=['POST'])
def add_task():

    try :
        data = request.json
        task_title = data.get('task_title')
        task_priority = data.get('task_priority')
        task_due_date = data.get('task_due_date')
        task_user_id = data.get('task_user_id')
        folder = data.get('folder')



        if task_title is None or task_priority is None or task_due_date is None or task_user_id is None or folder is None:
            return jsonify({'error': 'One or more variables are empty'}), 400

        sql_query = "INSERT INTO tasks (title, priority, due_date, userID, folder ,cheked) VALUES (?, ?, ?, ?, ?,0)"
    
        cursor.execute(sql_query, (task_title, task_priority, task_due_date, task_user_id, folder))

        conn.commit()


        return jsonify({'success': 'Data inserted successfully'}), 200
    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
    
@task_blueprint.route('/get_tasks_by_userID', methods=['POST'])
def get_tasks_by_userID():

    try :
        data = request.json
        task_user_id = data.get('task_user_id')


        if  task_user_id is None :
            return jsonify({'error': ' variable is empty'}), 400

        sql_query = "select * from tasks where userID = ?"
    
        cursor.execute(sql_query, ( task_user_id))

        tasks = cursor.fetchall()
        
        task_list = []
        for task_data in tasks:
            file_dict = {
                'taskId': task_data[0],
                'task_title': task_data[1],
                'Priority': task_data[2],
                'task_due_date': task_data[3],
                'userID': task_data[4],
                'folder': task_data[5],
                'checked' : task_data[6]
            }
            task_list.append(file_dict)

        return jsonify(task_list)

    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
    

@task_blueprint.route('/get_tasks_by_folder', methods=['POST'])
def get_tasks_by_folder():

    try :
        data = request.json
        folder= data.get('folder')


        if  folder is None :
            return jsonify({'error': ' variable is empty'}), 400

        sql_query = "select * from tasks where folder = ?"
    
        cursor.execute(sql_query, ( folder))

        tasks = cursor.fetchall()
        
        task_list = []
        for task_data in tasks:
            file_dict = {
                'taskId': task_data[0],
                'task_title': task_data[1],
                'Priority': task_data[2],
                'task_due_date': task_data[3],
                'userID': task_data[4],
                'folder': task_data[5],
                'checked': task_data[6],
            }
            task_list.append(file_dict)

        return jsonify(task_list)

    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
    

@task_blueprint.route('/get_task_by_id', methods=['POST'])
def get_tasks_by_id():

    try :
        data = request.json
        id= data.get('id')


        if  id is None :
            return jsonify({'error': ' variable is empty'}), 400

        sql_query = "select * from tasks where id = ?"
    
        cursor.execute(sql_query, ( id))

        task = cursor.fetchone()
        
        task_dict = {
                'taskId': task[0],
                'task_title': task[1],
                'Priority': task[2],
                'task_due_date': task[3],
                'userID': task[4],
                'folder': task[5],
                'checked': task[6],
            }

        return jsonify(task_dict)

    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
    

@task_blueprint.route('/delete_task', methods=['POST'])
def delete_task():

    try :
        data = request.json
        task_id= data.get('task_id')


        if  task_id is None :
            return jsonify({'error': ' variable is empty'}), 400

        sql_query = "DELETE FROM tasks WHERE id = ?;"
    
        cursor.execute(sql_query, ( task_id))

        conn.commit()
        return jsonify({'success': 'task delete successfully'}), 200

    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
    
@task_blueprint.route('/modify_task', methods=['Post'])
def modify_task():
    try:
        data = request.json

        task_id = data.get('task_id')
        task_title = data.get('task_title')
        task_priority = data.get('task_priority')
        task_due_date = data.get('task_due_date')
        task_user_id = data.get('task_user_id')
        folder = data.get('folder')

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = cursor.fetchone()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        cursor.execute("UPDATE tasks SET title=?, priority=?, due_date=?, userID=?, folder=? WHERE id=?",
                       (task_title, task_priority, task_due_date, task_user_id, folder, task_id,))

        conn.commit()

        return jsonify({'success': 'Task modified successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    
@task_blueprint.route('/modify_completion', methods=['Post'])
def modify_completion():
    try:
        data = request.json

        task_id = data.get('task_id')
        checked = data.get('checked')

        print(task_id , checked)

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = cursor.fetchone()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        cursor.execute("UPDATE tasks SET  cheked=? WHERE id=?",
                       ( checked,task_id,))

        conn.commit()

        return jsonify({'success': 'Task modified successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
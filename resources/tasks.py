from flask import Flask, request, jsonify,Blueprint
from datetime import datetime

from database import tasks

task_bp = Blueprint('routes-tasks', __name__)

@task_bp.route('/tasks', methods=['POST']) # URL o Endpoint 
def add_task():
    title = request.json['title']
    create_date = datetime.now().strftime("%x") # 5/22/2020

    data = (title, create_date)
    task_id = tasks.insert_task(data)
    
    if task_id:
        task = tasks.select_task_by_id(task_id)
        return jsonify({'task':task})
    return jsonify({'message':'Internal Error'})

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():#Obtengo todos mis datos
    data = tasks.select_all_task()

    if data:
        return jsonify({'tasks': data})
    elif data == False:
        return jsonify({'message': 'Internal Error'})
    else:
        return jsonify({'tasks':{}})

@task_bp.route('/tasks', methods=['PUT'])
def update_task():
    title = request.json['title']
    #obtener id
    id_arg = request.args.get('id')

    if tasks.update_task(id_arg, (title,)):
        task = tasks.select_task_by_id(id_arg)
        return jsonify(task)
    return jsonify({"message":"Error Fatal"})

@task_bp.route('/tasks', methods=['DELETE'])
def delete_task():
    id_arg = request.args.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({'message':"Task Deleted"})
    return jsonify({"message": "Internal Error"})

@task_bp.route('/tasks/completed', methods=['PUT'])
def completed_task():
    id_arg = request.args.get('id')
    completed = request.args.get('completed')

    if tasks.complete_tasks(id_arg, completed):
        return jsonify({"message":"Succesfully"})
    return jsonify({"message": "Internal Error"})

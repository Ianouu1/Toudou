import datetime
import io
import os

from datetime import datetime
import click
import uuid
from toudou import models
from toudou import services
from flask import Flask, render_template, request, redirect, url_for, send_file, Blueprint


@click.group()
def cli():
    pass


@cli.command()
def init_db():
    models.init_db()


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.", )
@click.option("-d", "--description", prompt="Description of the task", help="Add a description to a task")
@click.option("-da", "--date", prompt="Task due date (YYYY-MM-DD HH:MM:SS)",
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              help="Add a due to the task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Task status (True, False)", type=bool,
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def createTask(task: str, description: str, date: datetime, status: bool):
    models.createTask(None, task, description, date, bool(status))


@cli.command()
def createTaskTest():
    models.createTaskTest()


@cli.command()
@click.option("-i", "--id", prompt="Task ID", type=click.UUID, help="The id of a task")
@click.option("-t", "--task", prompt="Task Name", help="The task to remember")
@click.option("-d", "--description", prompt="Task Description", help="Add a description to a task")
@click.option("-da", "--date", prompt="Task Due Date (YYYY-MM-DD HH:MM:SS)",
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Task Status (True, False)", type=bool,
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def updateTask(id: uuid.UUID, task: str, description: str, date: datetime, status: bool):
    models.updateTask(id, task, description, date, status)


@cli.command()
@click.option("-i", "--id", prompt="Task ID", type=click.UUID, help="The id of a task")
def deleteTask(id: uuid.UUID):
    models.deleteTask(id)


@cli.command()
@click.option("-i", "--id", prompt="Task ID", type=click.UUID, help="The id of a task")
def readOneTask(id: uuid.UUID):
    todo = models.getOneTask(id)
    if todo:
        print("-------- Here is the requested task -------- \n")
        print(f"ID: {todo.id}")
        print(f"Task: {todo.task}")
        print(f"Description: {todo.description}")
        print(f"Date: {todo.date}")
        print(f"Status: {todo.status} \n")
        print("-------------------------------------------- ")
    else:
        print("No task could be found")


@cli.command()
def readAllTasks():
    todos = models.getAllTasks()
    if todos:
        print("-------- Here is the list of tasks -------- \n")
        for todo in todos:
            print(f"ID: {todo.id}")
            print(f"Task: {todo.task}")
            print(f"Description: {todo.description}")
            print(f"Date: {todo.date}")
            print(f"Status: {todo.status} \n")
        print("------------------------------------------ ")
    else:
        print("No task could be found")


@cli.command()
@click.option("--csv-file", type=click.File("r"), default="exportedata.csv",
              prompt="Name of the file",
              help="The name of the csv file")
def import_csv(csv_file):
    services.import_from_csv(csv_file)


@cli.command()
def export_csv():
    click.echo(services.export_to_csv())

web_ui = Blueprint("web_ui", __name__, url_prefix="/")



@web_ui.route('/')
def index():
    todos = models.getAllTasks()
    return render_template("index.html", todos=todos)


@web_ui.route('/create')
def show_create_form():
    todos = models.getAllTasks()
    message = request.args.get('message')
    return render_template('toudou-action.html', todos=todos, action='create', message=message)


@web_ui.route('/create', methods=['POST'])
def create_task():
    task = request.form['taskName']
    description = request.form['taskDescription']
    if 'taskDatetime' in request.form and request.form['taskDatetime']:
        date = datetime.strptime(request.form['taskDatetime'], "%Y-%m-%dT%H:%M")
    else:
        date = None
    status = request.form['taskStatus'].lower() == "true"
    message = models.createTask(None, task, description, date, status)
    if message:
        message = "success"
    else:
        message = "failed"
    return redirect(url_for('show_create_form', message=message))


@web_ui.route('/update')
def show_update_form():
    todos = models.getAllTasks()
    message = request.args.get('message')
    return render_template('toudou-action.html', todos=todos, action='update', message=message)


@web_ui.route('/update', methods=['POST'])
def update_task():
    taskId = uuid.UUID(request.form['taskId'])
    newTaskName = request.form['newTaskName']
    newDescription = request.form['newDescription']
    if 'newDatetime' in request.form and request.form['newDatetime']:
        newDatetime = datetime.strptime(request.form['newDatetime'], "%Y-%m-%dT%H:%M")
    else:
        newDatetime = None
    newStatus = request.form['newStatus'].lower() == "true"
    message = models.updateTask(taskId, newTaskName, newDescription, newDatetime, newStatus)
    if message:
        message = "success"
    else:
        message = "failed"
    return redirect(url_for('show_update_form', message=message))


@web_ui.route('/delete')
def show_delete_form():
    todos = models.getAllTasks()
    message = request.args.get('message')
    return render_template('toudou-action.html', todos=todos, action='delete', message=message)


@web_ui.route('/delete', methods=['POST'])
def delete_task():
    taskId = uuid.UUID(request.form['deleteTaskId'])
    message = models.deleteTask(taskId)
    if message:
        message = "success"
    else:
        message = "failed"
    return redirect(url_for('show_delete_form', message=message))


@web_ui.route('/id')
@web_ui.route("/id/<todoid>")
def viewTodo(todoid=None):
    todo = models.getOneTask(uuid.UUID(todoid))
    return render_template('toudou-view.html', todo=todo)


@web_ui.route('/csv')
def viewCSV():
    message = request.args.get('message')
    return render_template('toudou-csv.html', message=message)


@web_ui.route('/export_csv', methods=['POST'])
def export_csv_gui():
    models.getAllTasks()
    if services.export_to_csv():
        message = "success_export"
    else:
        message = "failed_export"
    return redirect(url_for('viewCSV', message=message))


@web_ui.route('/import_csv', methods=['POST'])
def import_csv_gui():
    if 'file' not in request.files:
        return redirect(url_for('viewCSV', message="failed_import"))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('viewCSV', message="failed_import"))

    csv_content = io.StringIO(file.stream.read().decode("utf-8"), newline=None)

    services.import_from_csv(csv_content)

    return redirect(url_for('viewCSV', message="success_import"))


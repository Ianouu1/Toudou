import datetime
import io
import logging

from datetime import datetime
import click
import uuid

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.simple import TextAreaField, PasswordField

from toudou import models
from toudou import services
from flask import Flask, render_template, request, redirect, url_for, send_file, Blueprint, abort, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from spectree import SpecTree, SecurityScheme
from pydantic.v1 import BaseModel, Field, constr
from typing import Optional


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
def deleteAllTasks():
    models.deleteAllTasks()


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
api = Blueprint("api", __name__, url_prefix="/api")

spec = SpecTree(
    "flask",
    security_schemes=[
        SecurityScheme(
            name="bearer_token",
            data={"type": "http", "scheme": "bearer"}
        )
    ],
    security=[{"bearer_token": []}]
)
spec.register(web_ui)

authLogin = HTTPBasicAuth()
authToken = HTTPTokenAuth(scheme='Bearer')


# ---------------------- API ---------------------- #
@api.get("/todos")
@authToken.login_required()
@spec.validate(tags=["api"])
def api_get_todos():
    try:
        tasks = models.getAllTasks()
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.get("/todos/<id>")
@authToken.login_required()
@spec.validate(tags=["api"])
def api_get_todo(id):
    try:
        task = models.getOneTask(uuid.UUID(id))
        if task:
            return jsonify(task), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.delete("/todos/<id>")
@authToken.login_required()
@spec.validate(tags=["api"])
def api_delete_todo(id):
    try:
        success = models.deleteTask(uuid.UUID(id))
        if success:
            return jsonify({"message": "Task deleted successfully"}), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


class TaskCreateRequest(BaseModel):
    taskName: str = Field("Salut", title="Task Name", description="Name of the task")
    taskDescription: Optional[str] = Field(None, title="Description", description="Description of the task")
    taskDatetime: Optional[datetime] = Field(None, title="Date", description="Date and time of the task in ISO format")
    taskStatus: bool = Field(False, title="Status", description="Status of the task (True or False)")


@api.post("/todos")
@authToken.login_required()
@spec.validate(tags=["api"], json=TaskCreateRequest)
def api_create_todo(json: TaskCreateRequest):
    try:
        task = models.createTask(
            id=None,
            task=json.taskName,
            description=json.taskDescription,
            date=json.taskDatetime,
            status=json.taskStatus
        )
        if task:
            return jsonify({"message": "Task created successfully"}), 201, abort(201)
        else:
            return jsonify({"error": "Failed to create task"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------- Login ---------------------- #

@web_ui.route('/')
@authLogin.login_required
def index():
    todos = models.getAllTasks()
    return render_template("index.html", todos=todos)


users = {
    "user": generate_password_hash("user"),
    "u": generate_password_hash("u"),
    "a": generate_password_hash("a"),
    "admin": generate_password_hash("admin"),
    "flo": generate_password_hash("flo")
}

roles = {
    "user": ["user", "u"],
    "admin": ["admin", "a", "flo"]
}

tokens = {
    "token1": "john",
    "token2": "susan",
    "a": "florian"
}


@authToken.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@authLogin.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@authLogin.get_user_roles
def get_user_roles(user):
    if user in roles["admin"]:
        return ["admin"]
    elif user in roles["user"]:
        return ["user"]
    else:
        return []


@web_ui.route("/admin")
@authLogin.login_required(role="admin")
def admins_only():
    return f"Hello {authLogin.current_user()}, you are an admin!"


# ---------------------- GUI Create ---------------------- #
class createForm(FlaskForm):
    taskName = StringField('Task Name', validators=[DataRequired()])
    taskDescription = TextAreaField('Description')
    taskDatetime = DateTimeLocalField('Date', format='%Y-%m-%dT%H:%M')
    taskStatus = SelectField('Status', choices=[('False', 'False'), ('True', 'True')])


@web_ui.route('/create')
@authLogin.login_required(role="admin")
def show_create_form():
    todos = models.getAllTasks()
    form_create = createForm()
    message = request.args.get('message')
    return render_template('toudou-action.html', todos=todos, action='create', message=message, formCreate=form_create)


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
    return redirect(url_for('web_ui.show_create_form', message=message))


# ---------------------- GUI Update ---------------------- #
class updateForm(FlaskForm):
    taskId = StringField('New Task ID', validators=[DataRequired()])
    newTaskName = StringField('New Task Name', validators=[DataRequired()])
    newDescription = TextAreaField('New Description')
    newDatetime = DateTimeLocalField('New Date', format='%Y-%m-%dT%H:%M')
    newStatus = SelectField('New Status', choices=[('False', 'False'), ('True', 'True')])


@web_ui.route('/update')
@authLogin.login_required(role="admin")
def show_update_form():
    todos = models.getAllTasks()
    update_form = updateForm()
    message = request.args.get('message')
    return render_template('toudou-action.html', todos=todos, action='update', message=message, updateForm=update_form)


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
    return redirect(url_for('web_ui.show_update_form', message=message))


# ---------------------- GUI Delete ---------------------- #
class deleteForm(FlaskForm):
    deleteTaskId = StringField('Task ID', validators=[DataRequired()])


@web_ui.route('/delete')
@authLogin.login_required(role="admin")
def show_delete_form():
    todos = models.getAllTasks()
    delete_form = deleteForm()
    message = request.args.get('message')
    return render_template('toudou-action.html', todos=todos, action='delete', message=message, deleteForm=delete_form)


@web_ui.route('/delete', methods=['POST'])
def delete_task():
    taskId = uuid.UUID(request.form['deleteTaskId'])
    message = models.deleteTask(taskId)
    if message:
        message = "success"
    else:
        message = "failed"
    return redirect(url_for('web_ui.show_delete_form', message=message))


# ---------------------------------------------------- #

@web_ui.route('/id')
@web_ui.route("/id/<todoid>")
@authLogin.login_required(role="admin")
def viewTodo(todoid=None):
    todo = models.getOneTask(uuid.UUID(todoid))
    return render_template('toudou-view.html', todo=todo)


@web_ui.route('/csv')
@authLogin.login_required(role="admin")
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
    return redirect(url_for('web_ui.viewCSV', message=message))


@web_ui.route('/import_csv', methods=['POST'])
def import_csv_gui():
    if 'file' not in request.files:
        return redirect(url_for('web_ui.viewCSV', message="failed_import"))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('web_ui.viewCSV', message="failed_import"))

    csv_content = io.StringIO(file.stream.read().decode("utf-8"), newline=None)

    services.import_from_csv(csv_content)

    return redirect(url_for('web_ui.viewCSV', message="success_import"))


# ---------------------- Error Handlers ---------------------- #

@web_ui.errorhandler(500)
def handle_internal_error(error):
    flash("Internal server error", "error")
    logging.exception(error)
    return redirect(url_for("web_ui.index"))


@web_ui.errorhandler(404)
def handle_internal_error(error):
    flash("Page not found", "error")
    logging.exception(error)
    return redirect(url_for("web_ui.index"))


@web_ui.errorhandler(403)
def handle_internal_error(error):
    flash("Forbidden", "error")
    logging.exception(error)
    return redirect(url_for("web_ui.index"))

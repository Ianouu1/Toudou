import datetime
import os

import click
import uuid
from toudou import models
from toudou import services
from flask import Flask, render_template


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
@click.option("--csv-file", type=click.File("r"), default="data/exportedata.csv",
              prompt="Name of the file (precise 'data/' first)",
              help="The name of the csv file located in 'data'(precise 'data/' first)")
def import_csv(csv_file):
    services.import_from_csv(csv_file)


@cli.command()
def export_csv():
    click.echo(services.export_to_csv())


app = Flask(__name__)


@app.route('/')
def index(id=None):
    todos = models.getAllTasks()
    return render_template("index.html", todos=todos)

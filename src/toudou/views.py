import datetime
import os

import click
import uuid
from toudou import models
from toudou import services


@click.group()
def cli():
    pass


@cli.command()
def init_db():
    models.init_db()


@cli.command()
@click.option("-t", "--task", prompt="Votre tache", help="The task to remember.", )
@click.option("-d", "--description", prompt="Description de la tache", help="Add a description to a task")
@click.option("-da", "--date", prompt="Date d'echeance de la tache (YYYY-MM-DD HH:MM:SS)",
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Status de la tache (True, False)", type=bool,
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def createTask(id: None, task: str, description: str, date: datetime, status: bool):
    models.createTask(id, task, description, date, bool(status))


@cli.command()
def createTaskTest():
    models.createTaskTest()


@cli.command()
@click.option("-i", "--id", prompt="L'identifiant de votre tache", type=click.UUID, help="The id of a task")
@click.option("-t", "--task", prompt="Nom de votre tache", help="The task to remember.")
@click.option("-d", "--description", prompt="Description de votre tache", help="Add a description to a task")
@click.option("-da", "--date", prompt="Date d'echeance de la tache (YYYY-MM-DD HH:MM:SS)",
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Status de la tache (True, False)", type=bool,
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def updateTask(id: uuid.UUID, task: str, description: str, date: datetime, status: bool):
    models.updateTask(id, task, description, date, status)


@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", type=click.UUID, help="The id of a task")
def deleteTask(id: uuid.UUID):
    models.deleteTask(id)


@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", type=click.UUID, help="The id of a task")
def readOneTask(id: uuid.UUID):
    todo = models.getOneTask(id)
    if todo:
        print("-------- Voici la tache demandée -------- \n")
        print(f"ID: {todo.id}")
        print(f"Tache: {todo.task}")
        print(f"Description: {todo.description}")
        print(f"Date: {todo.date}")
        print(f"Status: {todo.status} \n")
        print("------------------------------------------")
    else:
        print("Aucune tache n'a pu être trouvé")



@cli.command()
def readAllTasks():
    todos = models.getAllTasks()
    if todos:
        print("-------- Voici la liste des taches -------- \n")
        for todo in todos:
            print(f"ID: {todo.id}")
            print(f"Tache: {todo.task}")
            print(f"Description: {todo.description}")
            print(f"Date: {todo.date}")
            print(f"Status: {todo.status} \n")
        print("------------------------------------------ ")
    else:
        print("Aucune tache n'a pu être trouvé")


@cli.command()
@click.option("--csv-file", type=click.File("r"), default="data/exportedata.csv",
              prompt="Nom du fichier (préciser 'data/' avant)",
              help="Le nom du fichier csv localisé dans 'data'(préciser 'data/' avant)")
def import_csv(csv_file):
    services.import_from_csv(csv_file)

@cli.command()
def export_csv():
    click.echo(services.export_to_csv())

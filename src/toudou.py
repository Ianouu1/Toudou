import argparse
import calendar

import click
import uuid
import dbInteraction

from dataclasses import dataclass


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    description: str
    date: str
    status: str  # temporary string


@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--task", prompt="Votre tache", help="The task to remember.")
@click.option("-d", "--description", prompt="Description de la tache", help="Add a description to a task")
@click.option("-da", "--date", prompt="Date d'echeance de la tache (YYYY-MM-DD HH:MM:SS)",
              help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Status de la tache (True, False)",
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def createTask(task: str, description: str, date: str, status: bool):
    todo = Todo(uuid.uuid4(), task, description, date, status)
    click.echo(todo)
    dbInteraction.createTask(todo.id, todo.task, todo.description, todo.date, todo.status)


@cli.command()
def createTaskTest():
    dbInteraction.createTaskTest()


@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", help="The id of a task")
@click.option("-t", "--task", prompt="Votre tache", help="The task to remember.")
@click.option("-d", "--description", prompt="Description de la tache", help="Add a description to a task")
@click.option("-da", "--date", prompt="Date d'echeance de la tache (YYYY-MM-DD HH:MM:SS)",
              help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Status de la tache (True, False)",
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def updateTask(id: str, task: str, description: str, date: str, status: bool):
    todo = Todo(id, task, description, date, status)
    click.echo(todo)
    dbInteraction.updateTask(todo.id, todo.task, todo.description, todo.date, todo.status)


@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", help="The id of a task")
def deleteTask(id: str):
    click.echo("Id de la tache qui va être supprimée : {}".format(id))
    dbInteraction.deleteTask(id)


@cli.command()
def readAllTasks():
    click.echo("Lecture de toutes les taches sous le format : 'id', 'tache', 'description', 'date de fin', 'status'")
    dbInteraction.readAllTasks()


@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", help="The id of a task")
def readOneTask(id: str):
    click.echo("Id de la tache qui va être lue : {}".format(id))
    dbInteraction.readOneTask(id)


@cli.command()
def exportCSV():
    click.echo("Export du CSV..")
    dbInteraction.exportcsv()
@cli.command()
@click.option("-file", "--file", prompt="Si on veut utiliser un fichier", help="if we want to use a file located in "
                                                                               "data/, (yes, no)")
@click.option("-d", "--data", prompt="Data en brut (Si on utilise un fichier ecrit n'importe quoi)", help="Raw of your data (example : "
                                                          "fb0f8c39-4554-4d37-a4b1-1f34092a3af9,task,desc,2024-03-21 "
                                                          "08:30:00,1")
def importCSV(data: str, file: str):
    if file.lower() == "yes":
        if not data:
            click.echo("You have chosen to use a file but did not provide data. Please provide data.")
            return
        click.echo("Import du CSV avec les données...")
        dbInteraction.importcsv(data, file)
    elif file.lower() == "no":
        click.echo("Import du CSV sans fichier...")
        dbInteraction.importcsv(data, None)
    else:
        click.echo("Invalid choice for file. Please choose 'yes' or 'no'.")

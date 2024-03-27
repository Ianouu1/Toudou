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
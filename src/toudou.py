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
    status: str # temporary string


@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--task", prompt="Votre tache", help="The task to remember.")
@click.option("-d", "--description", prompt="Description de la tache", help="Add a description to a task")
@click.option("-da", "--date", prompt="Date d'echeance de la tache (YYYY-MM-DD HH:MM:SS)", help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Status de la tache (True, False)", help="Add the curent status of a task (True: if finished, False: if not finished)")
def newTask(task: str, description: str, date: str, status: bool):
    todo = Todo(uuid.uuid4(), task, description, date, status)
    click.echo(todo)
    dbInteraction.registerTask(todo.id, todo.task, todo.description, todo.date, todo.status)

@cli.command()
def newTaskTest():
    dbInteraction.registerTaskTest()

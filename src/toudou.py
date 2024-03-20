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
@click.option("-da", "--date", prompt="Date d'echeance de la tache", help="Add an end date to a task (format: DD/MM/YYYY)")
@click.option("-s", "--status", prompt="Status de la tache", help="Add the curent status of a task (true: if finished, false: if not finished)")
def newTask(task: str, description: str, date: str, status: bool):
    todo = Todo(uuid.uuid4(), task, description, date, status)
    click.echo(todo)
    dbInteraction.registerTask(todo.id, todo.task, todo.description, todo.date, todo.status)



# Pour plus tard, si besoin. POur l'instant on met la date en string
# def parse_date(date_str):
#     try:
#         day, month, year = map(int, date_str.split('/'))
#         return day, month, year
#     except ValueError:
#         raise argparse.ArgumentTypeError("Mauvais format. Veuillez utiliser le format suivant : JJ/MM/AAAA.")

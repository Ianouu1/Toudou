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
@click.option("-t", "--task", prompt="Votre tache", help="The task to remember.")
@click.option("-d", "--description", prompt="Description de la tache", help="Add a description to a task")
@click.option("-da", "--date", prompt="Date d'echeance de la tache (YYYY-MM-DD HH:MM:SS)",
              help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Status de la tache (True, False)",
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def createTask(task: str, description: str, date: str, status: bool):
    models.createTask(uuid.uuid4(), task, description, date, bool(status))


@cli.command()
def createTaskTest():
    models.createTaskTest()


@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", help="The id of a task")
@click.option("-t", "--task", prompt="Votre tache", help="The task to remember.")
@click.option("-d", "--description", prompt="Description de la tache", help="Add a description to a task")
@click.option("-da", "--date", prompt="Date d'echeance de la tache (YYYY-MM-DD HH:MM:SS)",
              help="Add an end date to a task (YYYY-MM-DD HH:MM:SS)")
@click.option("-s", "--status", prompt="Status de la tache (True, False)",
              help="Add the curent status of a task (True: if finished, False: if not finished)")
def updateTask(id: str, task: str, description: str, date: str, status: bool):
    models.updateTask(id, task, description, date, status)


@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", help="The id of a task")
def deleteTask(id: str):
    models.deleteTask(id)

@cli.command()
@click.option("-i", "--id", prompt="l'identifiant de votre tache", help="The id of a task")
def readOneTask(id: str):
    models.readOneTask(id)


@cli.command()
def get_all():
    click.echo(models.readAllTasks())

@cli.command()
@click.argument("csv_file", type=click.File("r"))
def import_csv(csv_file):
    services.import_from_csv(csv_file)

@cli.command()
def export_csv():
    click.echo(services.export_to_csv())
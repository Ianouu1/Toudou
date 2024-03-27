import sqlite3
import uuid
from datetime import datetime


def convert_string_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


def registerTask(id: str, task: str, description: str, date: str, status: bool):
    try:
        con = sqlite3.connect(r"C:\Users\22206844\Desktop\toudou-0.1\data\mydata.db")
        cur = con.cursor()
        print("co")

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status c'est avec des 0 ou des 1 je crois
        print("create table")

        task_data = (str(id), task, description, date, status)
        task_data2 = ("OUAIS", "task", "description", convert_string_to_date('2024-03-21 08:30:00'), int(0))

        cur.execute("INSERT INTO toudou (id, task, description, enddate, status) VALUES (?, ?, ?, ?, ?)", task_data)
        con.commit()
        print("Tâche enregistrée avec succès dans la base de données.")
    except sqlite3.Error as e:
        print("Erreur lors de l'enregistrement de la tâche :", e)
    finally:
        if con:
            con.close()


def registerTaskTest():
    """
    This function isn't useful.
    It helped me to know how to insert data in the database.
    """
    test_id = str(uuid.uuid4())
    test_task = "Tache"
    test_desc = "Description"
    test_date = convert_string_to_date('2024-03-21 08:30:00')

    registerTask(test_id, test_task, test_desc, test_date, True)
    test_id = "ouais"
    registerTask(test_id, test_task, test_desc, test_date, False)

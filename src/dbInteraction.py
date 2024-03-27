import sqlite3
import uuid


def registerTask(id: str, task: str, description: str, date: str, status: bool):
    try:
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1

        task_data = (str(id), task, description, date, status)

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
    Fonction inutile.
    Elle m'a aidée a comprendre comment enregistrer des données dans la base de données.
    """
    test_id = str(uuid.uuid4())
    test_task = "Tache"
    test_desc = "Description"
    test_date = "2024-03-21 08:30:00"

    registerTask(test_id, test_task, test_desc, test_date, True)
    test_id = "ouais"
    registerTask(test_id, test_task, test_desc, test_date, False)

import sqlite3
import uuid
import csv


def createTask(id: str, task: str, description: str, date: str, status: bool):
    try:
        # ----- DB Connexion ----- #
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1
        # ----- ------------ ----- #

        task_data = (str(id), task, description, date, status)
        cur.execute("INSERT INTO toudou (id, task, description, enddate, status) VALUES (?, ?, ?, ?, ?)", task_data)
        con.commit()
        print("Tâche enregistrée avec succès dans la base de données.")
    except sqlite3.Error as e:
        print("Erreur lors de l'enregistrement de la tâche :", e)
    finally:
        if con:
            con.close()


def createTaskTest():
    """
    This function isn't useful.
    It helped me to know how to insert data in the database.
    Also add some know data to the database, it's better for testing other functions
    """
    test_id = str(uuid.uuid4())
    test_task = "Tache"
    test_desc = "Description"
    test_date = "2024-03-21 08:30:00"

    createTask(test_id, test_task, test_desc, test_date, True)
    test_id = "ouais"
    createTask(test_id, test_task, test_desc, test_date, False)
    test_id = "coucou"
    createTask(test_id, test_task, test_desc, test_date, False)
    test_id = "salut"
    createTask(test_id, test_task, test_desc, test_date, False)
    test_id = "lala"
    createTask(test_id, test_task, test_desc, test_date, False)


def updateTask(id: str, task: str, description: str, date: str, status: bool):
    try:
        # ----- DB Connexion ----- #
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1
        # ----- ------------ ----- #
        cur.execute("SELECT id FROM toudou WHERE id = ?", (str(id),))
        existing_id = cur.fetchone()

        if existing_id:
            task_data = (task, description, date, status, str(id))
            cur.execute("UPDATE toudou SET task = ?, description = ?, enddate = ?, status = ? WHERE id = ?", task_data)
            con.commit()
            print("Tâche modifiée avec succès dans la base de données.")
        else:
            print("L'ID est mauvais")

    except sqlite3.Error as e:
        print("Erreur lors de la modification de la tâche :", e)
    finally:
        if con:
            con.close()


def deleteTask(id: str):
    try:
        # ----- DB Connexion ----- #
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1
        # ----- ------------ ----- #
        cur.execute("SELECT id FROM toudou WHERE id = ?", (str(id),))
        existing_id = cur.fetchone()

        if existing_id:
            task_data = (str(id))
            cur.execute("DELETE FROM toudou WHERE id = ?", (task_data,))
            con.commit()
            print("Tâche supprimée avec succès dans la base de données.")
        else:
            print("L'ID est mauvais")

    except sqlite3.Error as e:
        print("Erreur lors de la supression de la tâche :", e)
    finally:
        if con:
            con.close()


def readAllTasks():
    try:
        # ----- DB Connexion ----- #
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1
        # ----- ------------ ----- #
        cur.execute("SELECT * FROM toudou")
        allLines = cur.fetchall()
        for i in range(len(allLines)):
            print(allLines[i])

    except sqlite3.Error as e:
        print("Erreur lors de l'affichage de toutes les tâches :", e)
    finally:
        if con:
            con.close()


def readOneTask(id: str):
    try:
        # ----- DB Connexion ----- #
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1
        # ----- ------------ ----- #
        cur.execute("SELECT id FROM toudou WHERE id = ?", (str(id),))
        existing_id = cur.fetchone()

        if existing_id:
            task_data = (str(id))
            cur.execute("SELECT * FROM toudou WHERE id = ?", (task_data,))
            con.commit()
            task = cur.fetchone()
            print(task)
        else:
            print("L'ID est mauvais")

    except sqlite3.Error as e:
        print("Erreur lors de l'affichage de la tâche :", e)
    finally:
        if con:
            con.close()

def exportcsv():
    try:
        # ----- DB Connexion ----- #
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1
        # ----- ------------ ----- #

        cur.execute('SELECT * FROM toudou')

        data = cur.fetchall()
        csv_file = 'data/exported_data.csv'
        with open(csv_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([i[0] for i in cur.description])
            # Write the data rows
            csv_writer.writerows(data)
    except sqlite3.Error as e:
        print("Erreur lors de l'exportation en CSV de la BD :", e)
    finally:
        if con:
            con.close()

def importcsv(data: str):
    pass
    try:
        # ----- DB Connexion ----- #
        con = sqlite3.connect("data/mydata.db")
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, enddate TEXT, status INTEGER)"
        )
        # Pour le status, un booléen est stocké avec 0 ou 1
        # ----- ------------ ----- #

        with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for column in header:
            create_table_query += f"{column} TEXT,"
        create_table_query = create_table_query[:-1] + ")"
        cur.execute(create_table_query)
    except sqlite3.Error as e:
        print("Erreur lors de l'importation du CSV dans la BD :", e)
    finally:
        if con:
            con.close()
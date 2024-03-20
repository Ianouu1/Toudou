import sqlite3

def registerTask(id: str, task: str, description: str, date: str, status: bool):
    con = sqlite3.connect(r"C:\Users\22206844\Desktop\toudou-0.1\data\mydata.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS toudou(id TEXT PRIMARY KEY, task TEXT, description TEXT, date TEXT, status TEXT)")
    # Comment je dois enregistrer une date : YYYY-MM-DD HH:MM:SS.SSS
    # Pour le status c'est avec des 0 ou des 1 je crois

    task_data = (str(id), task, description, date, status)
    task_data2 = ("OUAIS", "task", "description", '2024-03-21', "0")
    cur.execute("INSERT INTO toudou (id, task, description, date, status) VALUES (?, ?, ?, ?, ?)", task_data)
    print("Tâche enregistrée avec succès dans la base de données.")
    con.close()
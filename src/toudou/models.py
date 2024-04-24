import sqlite3
import uuid

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, DateTime

db = None
db_url = 'data/mydata.db'
engine = create_engine(f"sqlite:///{db_url}", echo=True)
metadata = MetaData()

todos_table = Table(
    "toudou", metadata,
    Column("id", String, primary_key=True, default=str(uuid.uuid4)),
    Column("task", String, nullable=False),
    Column("description", String, nullable=False),
    Column("enddate", DateTime, nullable=False),
    Column("status", Boolean, nullable=False)
)
def get_db():
    global db
    if db is None:
        db = sqlite3.connect(db_url)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS toudou
            (
                id TEXT PRIMARY KEY not null,
                task TEXT not null,
                description TEXT not null ,
                enddate TEXT not null ,
                status INTEGER not null
            )
        """)

@dataclass
class Todo:
    id: uuid.UUID
    task: str
    description: str
    date: str
    status: str  # temporary string

    @classmethod
    def from_db(cls, id: str, task: str, description: str, enddate: str, status: int):
        return cls(
            id, # TODO : uuid.UUID(id) @ the end
            task,
            description,
            enddate,
            status
        )

def createTask(id: str, task: str, description: str, date: str, status: str) -> None:
    with engine.connect() as conn:
        conn.execute(todos_table.insert().values(id=str(id), task=task, description=description, enddate=datetime.strptime(date, "%Y-%m-%d %H:%M:%S"), status=status))
        conn.commit()
def updateTask(id: str, task: str, description: str, date: str, status: bool):
    with get_db() as db:
        existing_id = db.execute("SELECT id FROM toudou WHERE id = ?", (str(id),)).fetchone()
        if existing_id:
            task_data = (task, description, date, status, str(id))
            db.execute("UPDATE toudou SET task = ?, description = ?, enddate = ?, status = ? WHERE id = ?", task_data)
            print("Tâche modifiée avec succès dans la base de données.")
        else:
            print("L'ID est mauvais")

def deleteTask(id: str):
    with get_db() as db:
        existing_id = db.execute("SELECT id FROM toudou WHERE id = ?", (str(id),)).fetchone()
        if existing_id:
            task_data = (str(id))
            db.execute("DELETE FROM toudou WHERE id = ?", (task_data,))
            print("Tâche supprimée avec succès dans la base de données.")
        else:
            print("L'ID est mauvais")


def readAllTasks():
    with get_db() as db:
        result = db.execute("SELECT * FROM toudou").fetchall()
        return [
            Todo.from_db(r["id"], r["task"], r["description"], r["enddate"], r["status"]) for r in result
        ]


def readOneTask(id: str):
    with get_db() as db:
        task = db.execute("SELECT * FROM toudou WHERE id = ?", ((id),)).fetchone()
        if task:
            return Todo.from_db(task["id"], task["task"], task["description"], task["enddate"], task["status"])
        else:
            raise Exception("Todo not found")

def createTaskTest():
    """
    This function isn't useful.
    It helped me to know how to insert data in the database.
    Also add some know data to the database, it's better for testing other functions
    """
    test_id = str(uuid.uuid4())
    test_task = "TETZ2TETAZEAZGEBAZ"
    test_desc = "Description"
    test_date = "2024-03-21 08:30:00"

    createTask(test_id, test_task, test_desc, test_date, True)
    # createTask(test_id, test_task, test_desc, test_date, True)
    # test_id = "ouais"
    # createTask(test_id, test_task, test_desc, test_date, False)
    # test_id = "coucou"
    # createTask(test_id, test_task, test_desc, test_date, False)
    # test_id = "salut"
    # createTask(test_id, test_task, test_desc, test_date, False)
    # test_id = "lala"
    # createTask(test_id, test_task, test_desc, test_date, False)

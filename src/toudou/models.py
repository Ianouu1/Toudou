import sqlite3
import uuid

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, DateTime, Uuid

db = None
db_url = 'data/mydata.db'
engine = create_engine(f"sqlite:///{db_url}", echo=True)
metadata = MetaData()

todos_table = Table(
    "toudou", metadata,
    Column("id", Uuid, primary_key=True, default=uuid.uuid4),
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


def init_db() -> None:
    metadata.create_all(engine)

@dataclass
class Todo:
    id: uuid.UUID
    task: str
    description: str
    date: str
    status: bool  # temporary string

    @classmethod
    def from_db(cls, id: str, task: str, description: str, enddate: str, status: int):
        return cls(
            id,  # TODO : uuid.UUID(id) @ the end
            task,
            description,
            enddate,
            status
        )


def createTask(
        task: str,
        description: str,
        date: str | None,
        status: bool) -> None:
    init_db()
    stmt = todos_table.insert().values(task=task,
                                       description=description,
                                       enddate=datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
                                       status=status);
    with engine.begin() as conn:
        result = conn.execute(stmt)


def updateTask(id: uuid.UUID,
               task: str,
               description: str,
               date: str | None, #Todo : Le mettre en dateTime et pas en str
               status: bool):
    init_db()
    stmt = todos_table.update().where(todos_table.c.id == id).values(
        task=task,
        description=description,
        enddate=datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
        status=status
    )
    with engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            print("L'ID est mauvais")
        else:
            print("Tâche modifiée avec succès dans la base de données.")


def deleteTask(id: str):
    init_db()
    with get_db() as db:
        existing_id = db.execute("SELECT id FROM toudou WHERE id = ?", (str(id),)).fetchone()
        if existing_id:
            task_data = (str(id))
            db.execute("DELETE FROM toudou WHERE id = ?", (task_data,))
            print("Tâche supprimée avec succès dans la base de données.")
        else:
            print("L'ID est mauvais")


def readAllTasks():
    init_db()
    with get_db() as db:
        result = db.execute("SELECT * FROM toudou").fetchall()
        return [
            Todo.from_db(r["id"], r["task"], r["description"], r["enddate"], r["status"]) for r in result
        ]


def readOneTask(id: str):
    init_db()
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
    test_desc = "Description"
    test_date = "2024-03-21 08:30:00"
    for i in range(10):
        taskname = "tache de test numéro " + str(i + 1)
        if i % 2:
            createTask(taskname, test_desc, test_date, False)
        else:
            createTask(taskname, test_desc, test_date, True)
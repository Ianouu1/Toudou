import os
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
    Column("id", Uuid, primary_key=True, default=uuid.uuid4, nullable=False),
    Column("task", String, nullable=False),
    Column("description", String, nullable=True),
    Column("enddate", DateTime, nullable=True),
    Column("status", Boolean, nullable=False)
)


def get_db():
    global db
    if db is None:
        db = sqlite3.connect(db_url)
        db.row_factory = sqlite3.Row
    return db


def init_db() -> None:
    if not db_exists():
        metadata.create_all(engine)


def db_exists():
    return os.path.exists(db_url)


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    description: str
    date: datetime
    status: bool

    @classmethod
    def from_db(cls, id: uuid.uuid4(), task: str, description: str, enddate: datetime, status: int):
        return cls(
            id,
            task,
            description,
            enddate,
            status
        )


def createTask(
        id: uuid.UUID | None,
        task: str,
        description: str | None,
        date: datetime | None,
        status: bool
) -> int:
    init_db()
    with engine.begin() as conn:
        if id is None:
            id = uuid.uuid4()
        stmt = todos_table.insert().values(id=id,
                                           task=task,
                                           description=description,
                                           enddate=date,
                                           status=status);
        result = conn.execute(stmt)
        conn.commit()
        return 1

def updateTask(
        id: uuid.UUID,
        task: str,
        description: str | None,
        date: datetime | None,
        status: bool
) -> int:
    init_db()
    with engine.connect() as conn:
        stmt = todos_table.update().where(todos_table.c.id == id).values(
            task=task,
            description=description,
            enddate=date,
            status=status
        )
        result = conn.execute(stmt)
        conn.commit()
        if result.rowcount == 0:
            return 0
        else:
            return 1


def deleteTask(id: uuid.UUID) -> int:
    init_db()
    with engine.begin() as conn:
        stmt = todos_table.delete().where(todos_table.c.id == id)
        result = conn.execute(stmt)
        conn.commit()
        if result.rowcount == 0:
            return 0
        else:
            return 1


def getAllTasks() -> list:
    init_db()
    with engine.begin() as conn:
        stmt = todos_table.select()
        result = conn.execute(stmt)
        todos = []
        for row in result.fetchall():
            todo = Todo(
                id=row[0],
                task=row[1],
                description=row[2],
                date=row[3],
                status=row[4]
            )
            todos.append(todo)
        return todos


def getOneTask(id: uuid.UUID):
    init_db()
    with engine.begin() as conn:
        stmt = todos_table.select().where(todos_table.c.id == id)
        result = conn.execute(stmt).fetchone()
        todo = None
        if result:
            todo = Todo(
                id=result[0],
                task=result[1],
                description=result[2],
                date=result[3],
                status=result[4]
            )
        return todo


def createTaskTest():
    """
    This function is not useful in the context of the todolist.
    It helped me to test inserts in the database
    """
    test_desc = "Description"
    test_date = "2024-03-21 08:30:00"
    test_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    for i in range(10):
        taskname = "Test Task N°" + str(i + 1)
        if i % 2:
            createTask(None,taskname, test_desc, test_date, False)
        else:
            createTask(None, taskname, test_desc, test_date, True)

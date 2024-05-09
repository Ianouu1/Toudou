import csv
import dataclasses
import io
import uuid
from datetime import datetime

from toudou import models
from toudou.models import createTask, Todo


def export_to_csv() -> bool:
    csv_file_path = 'data/exportedata.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as output:
        csv_writer = csv.DictWriter(
            output, fieldnames=[f.name for f in dataclasses.fields(Todo)]
        )
        csv_writer.writeheader()
        for todo in models.getAllTasks():
            csv_writer.writerow(dataclasses.asdict(todo))
        return True


def import_from_csv(csv_file: io.StringIO) -> None:
    models.init_db()
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        createTask(
            id=uuid.UUID(row["id"]),
            task=row["task"],
            description=row["description"],
            date=datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"),
            status = row["status"].lower() == "true"
        )
    return True
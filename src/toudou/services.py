import csv
import dataclasses
import io

from toudou.models import createTask, readAllTasks, Todo


def export_to_csv() -> io.StringIO:
    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output, fieldnames=[f.name for f in dataclasses.fields(Todo)]
    )
    csv_writer.writeheader()
    for todo in readAllTasks():
        csv_writer.writerow(dataclasses.asdict(todo))
    return output


def import_from_csv(csv_file: io.StringIO) -> None:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        createTask(
            task=row["task"],
            description=row["description"],
            date=row["enddate"],
            status=row["status"] == "True",
        )
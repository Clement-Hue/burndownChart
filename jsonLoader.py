from task import Task, ListTasks
from burndown import Burndown
import datetime
import ntpath
import json

class JsonLoader:
    def __init__(self, filename):
        self.filename = filename

    def to_date(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()

    def load_burden(self) -> Burndown:
        with open(self.filename) as json_file:
            data = json.load(json_file)
            tasks = []
            for task in data["tasks"]:
                if task["date"] is not None:
                    task["date"] = self.to_date(task["date"])
                tasks.append(Task(id=task["id"], task=task["task"], date=task["date"], point=task["point"],
                                  assign=task["assign"]))
            return Burndown(
                debut=self.to_date(data["debut"]), fin=self.to_date(data["fin"]), listTask=ListTasks(tasks), loader=self,
                image_file=f"./burndown/{ntpath.basename(self.filename).split('.')[0]}")

    def write_burden(self, burden:Burndown):
        def converter(o):
            if isinstance(o, datetime.date):
                return o.__str__()
            if isinstance(o, Task):
                return o.__dict__
            if isinstance(o, ListTasks):
                return o.tasks
        with open(self.filename, 'w') as json_file:
            json.dump({"debut": burden.debut, "fin": burden.fin, "tasks": burden.listTask}, json_file, default=converter)

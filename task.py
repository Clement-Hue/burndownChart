import datetime


class Task:
    def __init__(self, task:str, point: int, date=None, id=None):
        self.id = id
        self.task = task
        self.date = date
        self.point = point

    def done(self, date):
        self.date = date

    def __str__(self):
        string = ''
        string += f"id {self.id} {self.task} {self.point}"
        if self.date:
            string += f" fait le {self.date}"
        return string

    def __eq__(self, other):
        return self.id == other.id and self.date == other.date and self.task == other.task and \
               self.point == other.point


class ListTasks:
    def __init__(self, tasks=None):
        if tasks is None:
            tasks = []
        self.cpt = max((t.id for t in tasks), default=0)
        self.tasks = tasks
        self.burden = None

    def notify(self):
        if self.burden:
            self.burden.notify()

    def __eq__(self, other):
        return other.tasks == self.tasks

    def __str__(self):
        string = ""
        for task in self.tasks:
            string += task.__str__()
            string += "\n"
        return string

    def add_task(self, task):
        self.cpt += 1
        self.tasks.append(task)
        task.id = self.cpt
        self.notify()

    def remove_task(self, id):
        task = next((task for task in self.tasks if task.id == id), None)
        self.tasks.remove(task)
        self.notify()

    def get_storypoint(self):
        point = 0
        for task in self.tasks:
            point += task.point
        return point

    def task_done(self, id, date=datetime.date.today()):
        task = next((task for task in self.tasks if task.id == id), None)
        task.done(date)
        self.notify()


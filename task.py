import datetime


class Task:
    def __init__(self, task:str, point: int, date=None, id=None, assign=None):
        self.id = id
        self.task = task
        self.date = date
        self.point = point
        self.assign = assign

    def done(self, date):
        self.date = date

    def __str__(self):
        string = ''
        string += f"id {self.id} {self.task} {self.point}"
        if self.assign:
            string += f" {self.assign}"
        if self.date:
            string += f" fait le {self.date}"
        return string

    def __eq__(self, other):
        return self.id == other.id and self.date == other.date and self.task == other.task and \
               self.point == other.point and self.assign == other.assign


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
        for person, story_point in self.total_story_point_per_person().items():
            if person is None:
                person = "Général"
            string += f"{person} {story_point} points "
        return string

    def add_task(self, task):
        self.cpt += 1
        task.id = self.cpt
        self.tasks.append(task)
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

    def set_task_done(self, id, date=datetime.date.today()):
        task = next((task for task in self.tasks if task.id == id), None)
        task.done(date)
        self.notify()

    def list_person(self):
        persons = set()
        for task in self.tasks:
            persons.add(task.assign)
        return persons

    def total_story_point_per_person(self):
        story_point = {}
        for task in self.tasks:
            story_point[task.assign] = 0
        for task in self.tasks:
            story_point[task.assign] += task.point
        return story_point

    def story_point_per_person_done(self):
        story_point = {}
        for task in self.tasks:
            story_point[task.assign] = 0
        for task in self.tasks:
            if task.date is not None:
                story_point[task.assign] += task.point
        return story_point


    def progression(self):
        total = self.total_story_point_per_person()
        progress = self.story_point_per_person_done()
        for person in progress:
            progress[person] /= total[person]
            progress[person] *= 100
        return progress







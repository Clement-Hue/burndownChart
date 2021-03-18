import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, date2num,
                              rrulewrapper, RRuleLocator, drange)
import datetime
from functools import reduce
import json
from datetime import date, timedelta

class ID:
    cpt = 0

    @classmethod
    def gen(cls):
        cls.cpt += 1
        return cls.cpt


def to_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()

def write_data():
    with open('test.json', 'w') as json_file:
        json.dump({"debut": DEBUT, "fin": FIN, "tasks": TASKS}, json_file)

def load_data(filename = "tasks.json"):
    with open(filename) as json_file:
        data = json.load(json_file)
        for task in data["tasks"]:
            if task["date"] is not None:
                task["date"] = to_date(task["date"])
        ID.cpt = data["tasks"][-1]["id"]
        return to_date(data["debut"]), to_date(data["fin"]), data["tasks"]

DEBUT, FIN, TASKS = load_data()

def add_task(task, point):
    TASKS.append({"id": ID.gen(), "task": task, "point": point, "date": None})

def task_done(id, date):
    task = next((task for task in TASKS if task["id"] == id), None)
    if not date:
        task["date"] = datetime.date.today()
    else:
        task["date"] = to_date(date)

def remove_task(id):
    task = next((task for task in TASKS if task["id"] == id), None)
    TASKS.remove(task)

def tasks_to_string():
    string = ''
    for task in TASKS:
        string += f"id {task['id']} {task['task']} {task['point']} "
        if task["date"]:
            string += f"fait le {task['date']}"
        string += '\n'
    return string


def get_number_storypoint(tasks):
    point = 0
    for task in tasks:
        point += task["point"]
    return point 

def create_courbe_effectif(tasks, story_point):
    dates = drange(DEBUT, datetime.date.today(), timedelta(days=1))
    effectif = []
    current = story_point
    for date in dates:
        points_done = [t["point"] for t in filter(lambda task: date2num(task['date']) == date, tasks)]
        current -= reduce(lambda t1, t2: t1 + t2, points_done, 0)
        effectif.append(current)
    plt.plot_date(dates, effectif, "r-")


def create_and_save(input = "tasks.json",output = "burndown"):
    formatter = DateFormatter('%m/%d/%y')
    STORY_POINT = get_number_storypoint(TASKS)
    fig, ax = plt.subplots()
    plt.plot_date([DEBUT, FIN], [STORY_POINT,0], "b-")
    create_courbe_effectif(TASKS, STORY_POINT)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.savefig(fname=output)
    return plt

def show():
    create_and_save().show()


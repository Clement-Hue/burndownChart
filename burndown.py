import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, date2num,
                              rrulewrapper, RRuleLocator, drange)
import numpy as np
import datetime
from functools import reduce
from datetime import date, timedelta
import shortuuid

class ID:
    cpt = 0
    def __init__(self):
        ID.cpt += 1
        self.id = ID.cpt

DEBUT = date(2021, 3, 12)
FIN = date(2021, 3, 25)
TASKS = [
    {"id": ID(),"task": "menu gauche", "date": date(2021,3,15), "point": 5},
    {"id": ID() ,"task": "ajout modif delete patient", "date": None, "point": 8},
    {"id": ID(), "task": "ajout modif doc", "date": date(2021,3,15), "point": 5},
    {"id":ID() ,"task": "ajout medecin", "date": None, "point": 3},
    {"id":ID(), "task": "recherche patient", "date": None, "point": 3},
    {"id":ID(), "task": "fiche patient / list appel", "date": None, "point": 5},
    {"id": ID(), "task": "page alerte", "date": None, "point": 5},
    {"id":ID() ,"task": "menu gauche", "date": date(2021,3,15), "point": 5},
    {"id":ID() ,"task": "ajout modif delete staff", "date": None, "point": 8},
    {"id":ID(), "task": "liste staff", "date": None, "point": 3},
    {"id": ID() ,"task": "ajout modif delete appel", "date": None, "point": 3},
    ]

def add_task(task, point):
    TASKS.append({"id": ID(), "task": task, "point": point, "date": None})

def task_done(id):
    task = next((task for task in TASKS if task["id"].id == id), None)
    task["date"] = datetime.date.today()

    
def tasks_to_string():
    string = ''
    for task in TASKS:
        string += f"id {task['id'].id} {task['task']} {task['point']} "
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


def create_and_save():
    # tick every 5th easter
    formatter = DateFormatter('%m/%d/%y')

    STORY_POINT = get_number_storypoint(TASKS)
    fig, ax = plt.subplots()
    plt.plot_date([DEBUT, FIN], [STORY_POINT,0], "b-")
    create_courbe_effectif(TASKS, STORY_POINT)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.savefig(fname='burndown')

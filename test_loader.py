from task import Task, ListTasks
import os
from burndown import Burndown
from jsonLoader import JsonLoader
import json
import shutil
import datetime
import unittest


class TestTask(unittest.TestCase):
    def test_load_json(self):
        loader = JsonLoader("test.json")
        burden = loader.load_burden()
        self.assertEqual(burden.debut, datetime.date(2021, 3, 12))
        self.assertEqual(burden.fin, datetime.date(2021, 3, 25))
        self.assertEqual(burden.listTask, ListTasks([
            Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 15), point=5, assign="Coco"),
            Task(id=2, task="ajout modif delete patient", point=8, assign="Coco"),
            Task(id=3, task="ajout modif doc", date=datetime.date(2021, 3, 15), point=5, assign="Baba"),
            Task(id=4, task="ajout medecin", date=None, point=3, assign=None),
            Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=3, assign="Baba"),
        ]))

    def test_write_json(self):
        debut = datetime.date(2020, 1, 10)
        fin = datetime.date(2020, 2, 20)
        tasks = ListTasks([
            Task(id=1, task="menu gauche", date=datetime.date(2020, 3, 15), point=5, assign="Baba"),
            Task(id=2, task="ajout modif delete patient", date=None, point=8, assign="Cle"),
            Task(id=3, task="ajout modif doc", date=datetime.date(2020, 3, 15), point=5),
            Task(id=5, task="recherche patient", date=datetime.date(2020, 3, 15), point=8)
        ])
        burden = Burndown(debut=debut, fin=fin, listTask=tasks)
        loader = JsonLoader("test_write.json")
        loader.write_burden(burden)
        with open("test_write.json") as json_file:
            data = json.load(json_file)
            self.assertEqual(data, {"debut": "2020-01-10", "fin": "2020-02-20",
                                    "tasks": [{"id": 1, "task": "menu gauche", "date": "2020-03-15", "point": 5,
                                               "assign": "Baba"},
                                              {"id": 2, "task": "ajout modif delete patient", "date": None, "point": 8,
                                               "assign": "Cle"},
                                              {"id": 3, "task": "ajout modif doc", "date": "2020-03-15", "point": 5,
                                               "assign": None},
                                              {"id": 5, "task": "recherche patient", "date": "2020-03-15", "point": 8,
                                               "assign": None}
                                              ]})

    def test_auto_write(self):
        shutil.copyfile("test.json", "temp.json")
        loader = JsonLoader("temp.json")
        burden = loader.load_burden()
        burden.listTask.add_task(Task(task="page accueil", point=12, assign="Cle"))
        assert loader.load_burden().listTask == ListTasks([
            Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 15), point=5, assign="Coco"),
            Task(id=2, task="ajout modif delete patient", point=8, assign="Coco"),
            Task(id=3, task="ajout modif doc", date=datetime.date(2021, 3, 15), point=5, assign="Baba"),
            Task(id=4, task="ajout medecin", date=None, point=3, assign=None),
            Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=3, assign="Baba"),
            Task(id=6, task="page accueil", date=None, point=12, assign="Cle")
        ])
        burden.listTask.remove_task(6)
        assert loader.load_burden().listTask == ListTasks([
            Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 15), point=5, assign="Coco"),
            Task(id=2, task="ajout modif delete patient", point=8, assign="Coco"),
            Task(id=3, task="ajout modif doc", date=datetime.date(2021, 3, 15), point=5, assign="Baba"),
            Task(id=4, task="ajout medecin", date=None, point=3, assign=None),
            Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=3, assign="Baba"),
        ])
        burden.listTask.task_done(2, datetime.date(2021, 3, 13))
        assert loader.load_burden().listTask == ListTasks([
            Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 15), point=5, assign="Coco"),
            Task(id=2, task="ajout modif delete patient", date=datetime.date(2021, 3, 13), point=8, assign="Coco"),
            Task(id=3, task="ajout modif doc", date=datetime.date(2021, 3, 15), point=5, assign="Baba"),
            Task(id=4, task="ajout medecin", date=None, point=3, assign=None),
            Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=3, assign="Baba"),
        ])
        os.remove("temp.json")

from freezegun import freeze_time
import os
from task import Task, ListTasks
from burndown import Burndown
import datetime
import unittest


class TestTask(unittest.TestCase):
    def test_string_representation(self):
        t1 = Task(id=1, task="ajout staff", point=8, date=datetime.date(2021, 3, 12))
        self.assertEqual(t1.__str__(), "id 1 ajout staff 8 fait le 2021-03-12")
        t2 = Task(id=2, task="ajout menu gauche", point=12)
        self.assertEqual(t2.__str__(), "id 2 ajout menu gauche 12")


    def test_add_task(self):
        liste = ListTasks([Task(id=4, task="ajout menu", point=8)])
        liste.add_task(Task(task="ajout doc", point=5))
        liste.add_task(Task(task="ajout patient", point=8))
        self.assertEqual(liste.tasks, [
            Task(id=4, task="ajout menu", point=8),
            Task(id=5, task="ajout doc", point=5),
            Task(id=6, task="ajout patient", point=8)
        ])

    def test_add_in_emtpy_list(self):
        liste = ListTasks()
        liste.add_task(Task(task="ajout doc", point=5))
        self.assertEqual(liste.tasks, [Task(id=1, task="ajout doc", point=5)])

    def test_remove(self):
        liste = ListTasks([Task(id=4, task="ajout menu", point=8)])
        liste.add_task(Task(task="ajout doc", point=5))
        liste.remove_task(5)
        self.assertEqual(liste.tasks, [
            Task(id=4, task="ajout menu", point=8),
        ])
        liste.add_task(Task(task="ajout doc", point=5))
        self.assertEqual(liste.tasks, [
            Task(id=4, task="ajout menu", point=8),
            Task(id=6, task="ajout doc", point=5)
        ])

    def test_number_storypiont(self):
        l1 = ListTasks([Task(id=4, task="ajout menu", point=8),
                        Task(id=5, task="ajout doc", point=5)
                        ])
        l1.add_task(Task(task="ajout patient", point=8))
        self.assertEqual(l1.get_storypoint(), 21)
        l2 = ListTasks([Task(id=4, task="ajout menu", point=12),
                        Task(id=5, task="ajout doc", point=21)
                        ])
        self.assertEqual(l2.get_storypoint(), 33)

    def test_task_done(self):
        liste = ListTasks([Task(id=4, task="ajout menu", point=8),
                          Task(id=5, task="ajout doc", point=5)
                          ])
        liste.task_done(5)
        self.assertEqual(liste.tasks[1], Task(id=5, task="ajout doc", point=5, date=datetime.date.today()))
        liste.task_done(4, datetime.date(2021, 3, 1))
        self.assertEqual(liste.tasks[0], Task(id=4, task="ajout menu", point=8, date=datetime.date(2021, 3, 1)))

    @freeze_time("2021-03-19")
    def test_courbe_effectif_current(self):
        burndown = Burndown(debut=datetime.date(2021, 3, 12), fin=datetime.date(2021, 3, 25),
                            listTask= ListTasks([
                            Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 15), point=5),
                            Task(id=2, task="ajout modif delete patient", point=8),
                            Task(id=3, task="ajout modif doc", date=datetime.date(2021, 3, 15), point=5),
                            Task(id=4, task="ajout medecin", date=None, point=3),
                            Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=3),
                        ]))
        assert burndown.create_courbe_effectif()[0] == [24,24,24,11,11,11,11,11]

    @freeze_time("2021-03-25")
    def test_courbe_effectif_finished(self):
        burndown = Burndown(debut=datetime.date(2021, 3, 12), fin=datetime.date(2021, 3, 20),
                            listTask=ListTasks([
                                Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 13), point=5),
                                Task(id=2, task="ajout modif delete patient", date=datetime.date(2021, 3 , 13), point=8),
                                Task(id=3, task="ajout modif doc", date=datetime.date(2021, 3, 15), point=5),
                                Task(id=4, task="ajout medecin", date=datetime.date(2021,3,20), point=8),
                                Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=5),
                            ]))
        assert burndown.create_courbe_effectif()[0] == [31, 18, 18, 8, 8, 8, 8, 8, 0]

    @freeze_time("2021-03-25")
    def test_save_plot(self):
        burndown = Burndown(debut=datetime.date(2021, 3, 12), fin=datetime.date(2021, 3, 20),
                            listTask=ListTasks([
                                Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 13), point=5),
                                Task(id=2, task="ajout modif delete patient", date=datetime.date(2021, 3 , 13), point=8),
                                Task(id=3, task="ajout modif doc", date=datetime.date(2021, 3, 15), point=5),
                                Task(id=4, task="ajout medecin", date=datetime.date(2021,3,20), point=8),
                                Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=5),
                            ]))
        burndown.create_chart("test")
        file = "./burndown/test.png"
        assert os.path.exists(file) is True
        os.remove(file)

    def test_list_task(self):
        listTask = ListTasks([
            Task(id=1, task="menu gauche", date=datetime.date(2021, 3, 13), point=5),
            Task(id=2, task="ajout modif delete patient", date=None, point=8),
            Task(id=3, task="ajout modif doc", date=None, point=5),
            Task(id=4, task="ajout medecin", date=None, point=8),
            Task(id=5, task="recherche patient", date=datetime.date(2021, 3, 15), point=5),
        ])
        assert listTask.__str__() == "id 1 menu gauche 5 fait le 2021-03-13\n" \
                                     "id 2 ajout modif delete patient 8\n"\
                                     "id 3 ajout modif doc 5\n"\
                                    "id 4 ajout medecin 8\n"\
                                    "id 5 recherche patient 5 fait le 2021-03-15\n"




import matplotlib.pyplot as plt
from matplotlib.dates import (DateFormatter, date2num,
                              drange)
import datetime
from functools import reduce
from task import ListTasks
from datetime import timedelta


class Burndown:
    def __init__(self, debut: datetime.date, fin: datetime.date, listTask: ListTasks, loader=None, image_file=None):
        self.loader = loader
        self.debut = debut
        self.fin = fin
        self.listTask = listTask
        self.listTask.burden = self
        self.image_file = image_file

    def notify(self):
        self.loader.write_burden(self)

    def create_courbe_effectif(self):
        fin = datetime.date.today() if datetime.date.today() < self.fin else self.fin
        dates = drange(self.debut, fin + timedelta(days=1), timedelta(days=1))
        effectif = []
        current = self.listTask.get_storypoint()
        for date in dates:
            points_done = [t.point for t in filter(lambda task: date2num(task.date) == date, self.listTask.tasks)]
            current -= reduce(lambda t1, t2: t1 + t2, points_done, 0)
            effectif.append(current)
        return effectif, dates

    def create_chart(self):
        formatter = DateFormatter('%m/%d/%y')
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_tick_params(rotation=30, labelsize=10)
        STORY_POINT = self.listTask.get_storypoint()
        effectif, dates = self.create_courbe_effectif()
        plt.plot_date([self.debut, self.fin], [STORY_POINT, 0], "b-")
        plt.plot_date(dates,effectif, "r-")
        plt.savefig(fname=self.image_file)
        return plt


    def progression(self):
        string = ""
        for person, percent in self.listTask.progression().items():
            string += f"{person}: {'{:.2f}'.format(percent)}% "
        return string

    def show(self):
        self.create_chart().show()




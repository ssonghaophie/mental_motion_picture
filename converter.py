from analyzer import *
from os import path
import pandas as pd


class Converter(object):
    col_names = ["sentence", "frame", "state change (act)", "entity", "act from", "act to", "container"]
    act_types = ["PTRANS", "PSTOP", "INGEST", "EXPEL", "STATECHANGE"]
    path = "dependency_graph.csv"

    def __init__(self, analyzer=None, model=None, dir=None, filename=None):
        if not analyzer and not model:
            raise Exception("No analyzer or model to convert!")
        if analyzer:
            self.model = analyzer.model
        else:
            self.model = model

        if filename:
            self.path = dir + "/" + filename
        self.df = pd.DataFrame(columns=self.col_names)

    def convert(self):
        """
        convert a mental motion picture to a csv file

        @return:
        """
        if path.exists(self.path):
            raise Exception("The file already exists.")

        frame = self.model.head
        frame_num = 1
        while frame:
            for act_type in self.act_types:
                for act in frame.actions_by_type[act_type]:
                    row = dict()
                    row[self.col_names[0]] = frame.sentence  # "sentence"
                    row[self.col_names[1]] = frame_num  # "frame"
                    row[self.col_names[2]] = act_type  # "state change (act)"
                    row[self.col_names[3]] = act.object  # "entity",
                    row[self.col_names[4]] = act.act_from  # "act from"
                    row[self.col_names[5]] = act.act_to  # "act to"
                    row[self.col_names[6]] = act.container  # "container"
                    self.df = pd.concat([self.df, pd.DataFrame(row)], ignore_index=True)

            frame_num += 1
            frame = frame.next

        self.df.to_csv(self.path)

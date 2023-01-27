from analyzer import *
from os import path
from datetime import datetime
import pandas as pd


class Converter(object):
    col_names = ["Sentence", "Frame", "State Change (act)", "Entity", "FromLoc", "ToLoc", "Container"]
    col_names_propara = ["Step", "State Change", "Entity", "FromLoc", "ToLoc"]
    act_types = ["PTRANS", "PSTOP", "INGEST", "EXPEL", "STATECHANGE"]

    def __init__(self, analyzer=None, model=None):
        if not (analyzer or model):
            raise Exception("No analyzer or model to convert!")
        if analyzer:
            self.model = analyzer.model
        else:
            self.model = model

        self.df = pd.DataFrame(columns=self.col_names)
        self.df_propara = None

    def convert(self, filename: str, date=False, dir=None):
        """
        convert a mental motion picture to a csv file

        @return:
        """
        if date:
            filename = str(datetime.date(datetime.now())) + filename
        save_path = dir + "/" + filename

        if path.exists(save_path):
            raise Exception("The file already exists.")

        frame = self.model.head
        frame_num = 1
        while frame:
            for act_type in self.act_types:
                for act in frame.actions_by_type[act_type]:
                    row = dict()
                    row[self.col_names[0]] = frame.sentence  # "Sentence"
                    row[self.col_names[1]] = frame_num  # "Frame"
                    row[self.col_names[2]] = act_type  # "State Change (act)"
                    row[self.col_names[3]] = act.object  # "Entity",
                    row[self.col_names[4]] = act.act_from  # "FromLoc"
                    row[self.col_names[5]] = act.act_to  # "ToLoc"
                    row[self.col_names[6]] = act.container  # "Container"
                    self.df = pd.concat([self.df, pd.DataFrame(row)], ignore_index=True)

            frame_num += 1
            frame = frame.next

        self.df.to_csv(save_path)

    def convert_propara_format(self, filename: str, date=False, dir=None):
        """
        convert a mental motion picture to a csv file that is more similar to
        the dependency graphs in the ProPara dataset.
        @return:
        """
        if date:
            filename = str(datetime.date(datetime.now())) + filename
        save_path = dir + "/" + filename

        if path.exists(save_path):
            raise Exception("The file already exists.")

        self.df_propara = pd.DataFrame(columns=self.col_names_propara)
        frame = self.model.head
        frame_num = 1
        while frame:
            for act_type in self.act_types:
                for act in frame.actions_by_type[act_type]:
                    row = dict()
                    row[self.col_names_propara[0]] = frame.sentence  # "Step"

                    # "State Change"
                    if act_type == "STATECHANGE":
                        row[self.col_names_propara[1]] = "Create"
                    else:
                        row[self.col_names_propara[1]] = "Move"

                    row[self.col_names_propara[2]] = act.object  # "Entity",

                    # "FromLoc"
                    if act_type == "EXPEL":
                        row[self.col_names_propara[3]] = act.container
                    else:
                        row[self.col_names_propara[3]] = act.act_from

                    # "ToLoc"
                    if act_type == "INGEST":
                        row[self.col_names_propara[4]] = act.container
                    else:
                        row[self.col_names_propara[4]] = act.act_to
                    self.df_propara = pd.concat([self.df_propara, pd.DataFrame(row)], ignore_index=True)

            frame_num += 1
            frame = frame.next

        self.df_propara.to_csv(save_path)

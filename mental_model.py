from map import Containment, Space, Touching
from primitive_acts import *
# from copy import deepcopy

"""
The Mental_map class is adapted from the linked_list class from
https://github.com/bfaure/Python3_Data_Structures/blob/master/Linked_List/main.py
"""


class Frame:

    def __init__(self, containment, space, touching):
        self.containment = containment
        self.space = space
        self.touching = touching
        self.actions = []
        self.actions_by_type = {"PTRANS": [], "PSTOP": [],
                                "INGEST": [], "EXPEL": [], "STATECHANGE": []}
        self.next = None
        self.empty = True  # only the initial state is empty


class MentalMotionPicture:
    def __init__(self):
        self.head = Frame(Containment(), Space(), Touching())
        self.count = 1  # number of Frames in this model
        self.cur = self.head  # the latest node

    def advance_time(self):
        """copy the current Frame to a new Frame"""
        self.count += 1
        new_node = Frame(self.cur.containment.copy(),
                         self.cur.space.copy(),
                         self.cur.touching.copy())

        # copy PTRANS actions to the new Frame
        if len(self.cur.actions_by_type["PTRANS"]) > 0:
            # instead of a deepcopy, we want a shallow copy of the ACT from the previous
            # Frame, so that is we update the PTRANS in the newest Frame,
            # the ACT stored in the previous Frame will also be updated.
            # new_node.action["PTRANS"] = deepcopy(self.cur.action["PTRANS"])
            new_node.actions_by_type["PTRANS"] = self.cur.actions_by_type["PTRANS"]

        if len(self.cur.actions_by_type["PSTOP"]) > 0:
            for action_s in self.cur.actions_by_type["PSTOP"]:
                for action_t in new_node.actions_by_type["PTRANS"]:
                    if action_t["object"] == action_s["object"]:
                        new_node.actions_by_type["PTRANS"].remove(action_t)
                        break
        new_node.empty = self.cur.empty
        self.cur.next = new_node
        self.cur = self.cur.next

        print(" - ADVANCE TO FRAME", self.count)

    def get(self, index):
        """Returns the value of the Frame at a certain index"""
        if index > self.count or index < 1:
            print("ERROR: Index out of range!")
            return None
        cur_idx = 1
        cur_node = self.head
        while True:
            if cur_idx == index:
                return cur_node
            cur_node = cur_node.next
            cur_idx += 1

    def get_containment(self, index):
        """Returns the containment map of the time_stamp at index"""
        return self.get(index).containment

    def get_space(self, index):
        """Returns the space map of the time_stamp at index"""
        return self.get(index).space

    def get_touching(self, index):
        """Returns the space map of the time_stamp at index"""
        return self.get(index).touching

    def add_object(self, object):
        """add object to all maps of the last Frame"""
        self.cur.containment.add_object(object)
        self.cur.space.add_object(object)
        self.cur.touching.add_object(object)
        self.cur.empty = False

    def contain(self, edge):
        """add an edge to the containment map of the last Frame"""
        self.cur.containment.contain(edge)
        self.cur.empty = False

    def x_contain(self, edge):
        """remove an edge from the containment map of the last Frame"""
        self.cur.containment.x_contain(edge)

    def above(self, edge):
        """add an edge to the space map of the last Frame"""
        self.cur.space.above(edge)
        self.cur.empty = False

    def x_above(self, edge):
        """remove an edge from the space map of the last Frame"""
        self.cur.space.x_above(edge)

    def under(self, edge):
        """add an edge to the space map of the last Frame"""
        self.cur.space.under(edge)
        self.cur.empty = False

    def x_under(self, edge):
        """remove an edge from the space map of the last Frame"""
        self.cur.space.x_under(edge)

    def touch(self, edge):
        """add an edge to the touching map of the last Frame"""
        # for object in edge:
        #     if object not in self.cur.containment._graph_dict:
        #         self.cur.containment.add_object(object)
        #         self.cur.space.add_object(object)
        #         self.cur.touching.add_object(object)
        self.cur.touching.touch(edge)
        self.cur.empty = False

    def x_touch(self, edge):
        """remove an edge from the touching map of the last Frame"""
        self.cur.touching.x_touch(edge)

    def print(self, index):
        """ print the containment map, space map, and touching map
            of the Frame at a certain index
        """
        print("\n-- -- -- -- print Frame", index)
        frame = self.get(index)

        print("\nCONTAINMENT RELATIONSHIP -------------------------------")
        print(frame.containment)

        print("\nSPATIAL RELATIONSHIP -----------------------------------")
        print(frame.space)

        print("\nTOUCHING RELATIONSHIP ----------------------------------")
        print(frame.touching)

        print("\nPRIMITIVE ACTIONS --------------------------------------")

        print("PTRANS: ", end="")
        for act in frame.actions_by_type["PTRANS"]:
            print("(objects:", act.object, ", from:", act.act_from, ", to:", act.act_to, end=") ")

        print("\nPSTOP: ", end="")
        for act in frame.actions_by_type["PSTOP"]:
            print("(objects:", act.object, end=") ")

        print("\nINGEST: ", end="")
        for act in frame.actions_by_type["INGEST"]:
            print("(objects:", act.object, ", container:", act.container, ", from:", act.act_from, end=") ")

        print("\nEXPEL: ", end="")
        for act in frame.actions_by_type["EXPEL"]:
            print("(objects:", act.object, ", container:", act.container, end=") ")

        print("\nSTATECHANGE: ", end="")
        for act in frame.actions_by_type["STATECHANGE"]:
            print("(objects:", act.object, ", to:", act.act_to, end=") ")

    def print_latest(self):
        self.print(self.count)

    def __getitem__(self, index):
        """Allows for bracket operator syntax (i.e. a[0] = first item)"""
        return self.get(index)

    def add_to_graph(self, object):
        """
        check if an object exists in the graph; if not, add to graph

        @param object:
        @return:
        """
        if object not in self.cur.containment._graph_dict:
            self.cur.containment.add_object(object)
            self.cur.space.add_object(object)
            self.cur.touching.add_object(object)

    def PTRANS(self, object, to=None, From=None):
        self.add_to_graph(object)

        act = PTRANS(object, act_from=From, act_to=to)
        self.cur.actions_by_type["PTRANS"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

    def PSTOP(self, object):
        self.add_to_graph(object)

        act = PSTOP(object)
        self.cur.actions_by_type["PSTOP"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

    def INGEST(self, object, container, ingest_from=None):
        for thing in [object, container, ingest_from]:
            self.add_to_graph(thing)

        act = INGEST(object, container=container, act_from=ingest_from)
        self.cur.actions_by_type["INGEST"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

    def EXPEL(self, object, container):
        for thing in [object, container]:
            self.add_to_graph(thing)

        act = EXPEL(object, container=container)
        self.cur.actions_by_type["EXPEL"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

    def STATECHANGE(self, object, to):
        for thing in [object, to]:
            self.add_to_graph(thing)

        act = STATECHANGE(object, act_to=to)
        self.cur.actions_by_type["STATECHANGE"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

    def update_act_by_type(self, act_type: str, key: str, val: str, index=None):
        """
        update the last primitive act of a type in a specific timestep

        @param act_type:
        @param key:
        @param val:
        @param index:
        @return:
        """
        # get the timestep that needs to be updated
        if not index:
            node = self.cur
        else:
            node = self.get(index)

        # update the last ACT of that type
        if key not in ["object", "from", "to", "container"]:
            print("Invalid primitive act attribute!")
            return
        if key == "object":
            node.actions_by_type[act_type][-1].object = [val]
        elif key == "from":
            node.actions_by_type[act_type][-1].act_from = val
        elif key == "to":
            node.actions_by_type[act_type][-1].act_to = val
        elif key == "container":
            node.actions_by_type[act_type][-1].container = val

    def update_act(self, key: str, val: str):
        """
        update the last primitive act of the model

        @param key:
        @param val:
        @return:
        """
        if key not in ["object", "from", "to", "container"]:
            print("Invalid primitive act attribute!")
            return

        if key == "object":
            self.cur.actions[-1].object = [val]
        elif key == "from":
            self.cur.actions[-1].act_from = val
        elif key == "to":
            self.cur.actions[-1].act_to = val
        elif key == "container":
            self.cur.actions[-1].container = val

    def update_act_add_object(self, val: str):
        """
        add an object to the last primitive act of the model

        @param val:
        @return:
        """
        self.cur.actions[-1].object.append(val)

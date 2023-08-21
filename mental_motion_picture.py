from map import Containment, Space, Touching
from noun_phrase import NounPhrase
from primitive_acts import *
from frame import Frame

"""
The Mental_map class is adapted from the linked_list class from
https://github.com/bfaure/Python3_Data_Structures/blob/master/Linked_List/main.py
"""


class MentalMotionPicture:
    cur_sentence = None

    def __init__(self):
        self.head = Frame(Containment(), Space(), Touching())
        self.count = 1  # number of Frames in this model
        self.cur = self.head  # the latest node

    # todo: add function to check for containment relationship in previous frames
    def check_containment_exist(self):
        a = self.count
        while a >= 1:
            result = self.get_containment(a)
            a = a - 1
            print("CHECKING: \nCHECKING IS HERE ")
            print(result)
            return result

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

        if self.cur.actions_by_type["PSTOP"]:
            for action_s in self.cur.actions_by_type["PSTOP"]:
                for action_t in new_node.actions_by_type["PTRANS"]:
                    if action_t.object == action_s.object:
                        new_node.actions_by_type["PTRANS"].remove(action_t)
                        break

        new_node.empty = self.cur.empty
        self.cur.next = new_node
        self.cur = self.cur.next
        self.cur.sentence = self.cur_sentence

        print(" - ADVANCE TO FRAME", self.count)

    def get(self, index: int):
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

    def get_containment(self, index) -> Containment:
        """Returns the containment map of the time_stamp at index"""
        return self.get(index).containment

    def get_space(self, index) -> Space:
        """Returns the space map of the time_stamp at index"""
        return self.get(index).space

    def get_touching(self, index) -> Touching:
        """Returns the space map of the time_stamp at index"""
        return self.get(index).touching

    def contain(self, edge: [str]):
        """add an edge to the containment map of the last Frame"""
        self.add_to_graph(edge[0])
        self.add_to_graph(edge[1])
        self.cur.containment.contain(edge)
        self.cur.empty = False

    def x_contain(self, edge: [str]):
        """remove an edge from the containment map of the last Frame"""
        self.cur.containment.x_contain(edge)

    def above(self, edge: [str]):
        """add an edge to the space map of the last Frame"""
        self.cur.space.above(edge)
        self.cur.empty = False

    def x_above(self, edge: [str]):
        """remove an edge from the space map of the last Frame"""
        self.cur.space.x_above(edge)

    def under(self, edge: [str]):
        """add an edge to the space map of the last Frame"""
        self.cur.space.under(edge)
        self.cur.empty = False

    def x_under(self, edge: [str]):
        """remove an edge from the space map of the last Frame"""
        self.cur.space.x_under(edge)

    def touch(self, edge: [str]):
        """add an edge to the touching map of the last Frame"""
        self.cur.touching.touch(edge)
        self.cur.empty = False

    def x_touch(self, edge: [str]):
        """remove an edge from the touching map of the last Frame"""
        self.cur.touching.x_touch(edge)

    def print(self, index: int):
        """ print the containment map, space map, and touching map of the Frame at a certain index"""
        frame = self.get(index)
        print("\n(Frame #" + str(index) + ")")

        print("\nCONTAINMENT RELATIONSHIP -------------------------------")
        print(frame.containment)

        print("\nSPATIAL RELATIONSHIP -----------------------------------")
        print(frame.space)

        print("\nTOUCHING RELATIONSHIP ----------------------------------")
        print(frame.touching)

        print("\nPRIMITIVE ACTIONS --------------------------------------")

        print("PTRANS: ", end="")
        for act in frame.actions_by_type["PTRANS"]:
            print(str(act), end=" ")

        print("\nPSTOP: ", end="")
        for act in frame.actions_by_type["PSTOP"]:
            print(str(act), end=" ")

        print("\nINGEST: ", end="")
        for act in frame.actions_by_type["INGEST"]:
            print(str(act), end=" ")

        print("\nEXPEL: ", end="")
        for act in frame.actions_by_type["EXPEL"]:
            print(str(act), end=" ")

        print("\nSTATECHANGE: ", end="")
        for act in frame.actions_by_type["STATECHANGE"]:
            print(str(act), end=" ")
        print("")

    def print_latest(self):
        self.print(self.count)

    def __getitem__(self, index):
        """Allows for bracket operator syntax (i.e. a[0] = first item)"""
        return self.get(index)

    def add_to_graph(self, obj: str):
        """
        check if an object exists in the graph; if not, add to graph;
        do not add None to the graph.

        @param obj:
        @return:
        """
        if obj and (obj not in self.cur.space.noun_dict):
            noun = NounPhrase(obj)
            self.cur.containment.add_object(noun)
            self.cur.space.add_object(noun)
            self.cur.touching.add_object(noun)
            self.cur.empty = False

    def ptrans(self, obj: str, to=None, act_from=None):
        self.add_to_graph(obj)
        containment_frame = self.get_containment(self.count)
        for edge in containment_frame.all_edges():
            if str(edge[1]) == obj:
                act_from = str(edge[0])

        act = Ptrans(obj, act_from=act_from, act_to=to)
        self.cur.actions_by_type["PTRANS"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

    def pstop(self, obj: str):
        self.add_to_graph(obj)

        act = Pstop(obj)
        self.cur.actions_by_type["PSTOP"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

    def ingest(self, obj: str, container: str, ingest_from=None):
        for thing in [obj, container, ingest_from]:
            self.add_to_graph(thing)

        act = Ingest(obj, container=container, act_from=ingest_from)
        self.cur.actions_by_type["INGEST"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

        # frame = self.get(self.count)
        # print(frame.containment)


    # if a thing is already ingested, set it as the container of expel function 
    # Virus ingests RNA, object:RNA, container:VIRUS
    # Virus expels RNA object:RNA, container: VIRUS
    def expel(self, obj: str, container: str, expel_to: str):
        for thing in [obj, container, expel_to]:
            self.add_to_graph(thing)
        containment_frame = self.get_containment(self.count)
        for edge in containment_frame.all_edges():
            if str(edge[1]) == obj:
                container = str(edge[0])  

        act = Expel(obj, container=container, act_to=expel_to)
        self.cur.actions_by_type["EXPEL"].append(act)
        self.cur.actions.append(act)

        self.cur.empty = False

        # CHANGE: delete containment when EXPEL gets called
        if container and obj:
            self.delete_contain(container,obj)

    # CHANGE: delete the containment relationship if it existed before and got expeled   
    def delete_contain(self, container: str, obj: str):
        #print(container, obj)
        con_relationship = "("+ container + " " + obj + ")"
        containment_frame = self.get_containment(self.count)
        #print("HI UPDATE EXPEL works")
        if con_relationship in str(containment_frame):
            for edge in containment_frame.all_edges():
                if str(edge[0]) == container and str(edge[1]) == obj:
                    #print("HI I delete containment")
                    containment_frame.x_contain([str(edge[0]),str(edge[1])])

    def state_change(self, obj: str, to: str):
        for thing in [obj, to]:
            self.add_to_graph(thing)

        act = StateChange(obj, act_to=to)
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
        
        #print(node.actions_by_type[act_type][-1].object)
        # CHANGE: delete containment when EXPEL gets updated
        container = node.actions_by_type[act_type][-1].container
        #print(node.actions_by_type[act_type][-1].object)
        obj = node.actions_by_type[act_type][-1].object[0]

        if act_type == "EXPEL" and container and obj:
            self.delete_contain(container, obj)

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
        if self.cur.actions:
            self.cur.actions[-1].object.append(val)
        
        #self.add_to_graph(val)

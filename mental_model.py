from map import Containment, Space, Touching
from copy import deepcopy

"""
The Mental_map class is adapted from the linked_list class from
https://github.com/bfaure/Python3_Data_Structures/blob/master/Linked_List/main.py
"""


class Frame:

    def __init__(self, containment, space, touching):
        self.containment = containment
        self.space = space
        self.touching = touching
        self.action = {"PTRANS": [], "PSTOP": [],
                       "INGEST": [], "EXPEL": [], "STATECHANGE": []}
        self.next = None
        self.empty = True  # only the initial state is empty


class Mental_motion_picture:
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
        if len(self.cur.action["PTRANS"]) > 0:
            # instead of a deepcopy, we want a shallow copy of the ACT from the previous
            # Frame, so that is we update the PTRANS in the newest Frame,
            # the ACT stored in the previous Frame will also be updated.
            # new_node.action["PTRANS"] = deepcopy(self.cur.action["PTRANS"])
            new_node.action["PTRANS"] = self.cur.action["PTRANS"]

        if len(self.cur.action["PSTOP"]) > 0:
            for action_s in self.cur.action["PSTOP"]:
                for action_t in new_node.action["PTRANS"]:
                    if action_t["object"] == action_s["object"]:
                        new_node.action["PTRANS"].remove(action_t)
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
        # for object in edge:
            # if object not in self.cur.containment._graph_dict:
            #     self.cur.containment.add_object(object)
            #     self.cur.space.add_object(object)
            #     self.cur.touching.add_object(object)
        self.cur.containment.contain(edge)
        self.cur.empty = False

    def x_contain(self, edge):
        """remove an edge from the containment map of the last Frame"""
        self.cur.containment.x_contain(edge)

    def above(self, edge):
        """add an edge to the space map of the last Frame"""
        # for object in edge:
            # if object not in self.cur.containment._graph_dict:
            #     self.cur.containment.add_object(object)
            #     self.cur.space.add_object(object)
            #     self.cur.touching.add_object(object)
        self.cur.space.above(edge)
        self.cur.empty = False

    def x_above(self, edge):
        """remove an edge from the space map of the last Frame"""
        self.cur.space.x_above(edge)

    def under(self, edge):
        """add an edge to the space map of the last Frame"""
        # for object in edge:
        #     if object not in self.cur.containment._graph_dict:
        #         self.cur.containment.add_object(object)
        #         self.cur.space.add_object(object)
        #         self.cur.touching.add_object(object)
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
        for action in frame.action:
            print(action, frame.action[action])

    def print_latest(self):
        self.print(self.count)

    def __getitem__(self, index):
        """Allows for bracket operator syntax (i.e. a[0] = first item)"""
        return self.get(index)

    def PTRANS(self, object, to=None, From=None):
        if object not in self.cur.containment._graph_dict:
            self.cur.containment.add_object(object)
            self.cur.space.add_object(object)
            self.cur.touching.add_object(object)

        # new_dict = ["object " + object, "from " + From, "to " + to]
        new_dict = {"object": object, "from": From, "to": to}
        self.cur.action["PTRANS"].append(new_dict)
        self.cur.empty = False

    def PSTOP(self, object):
        if object not in self.cur.containment._graph_dict:
            self.cur.containment.add_object(object)
            self.cur.space.add_object(object)
            self.cur.touching.add_object(object)

        self.cur.action["PSTOP"].append({})
        self.cur.action["PSTOP"][-1]["object"] = object
        self.cur.empty = False

    def INGEST(self, object, container):
        for thing in [object, container]:
            if thing not in self.cur.containment._graph_dict:
                self.cur.containment.add_object(thing)
                self.cur.space.add_object(thing)
                self.cur.touching.add_object(thing)

        self.cur.action["INGEST"].append({})
        self.cur.action["INGEST"][-1]["object"] = object
        self.cur.action["INGEST"][-1]["container"] = container
        self.cur.empty = False

    def EXPEL(self, object, container):
        for thing in [object, container]:
            if thing not in self.cur.containment._graph_dict:
                self.cur.containment.add_object(thing)
                self.cur.space.add_object(thing)
                self.cur.touching.add_object(thing)

        self.cur.action["EXPEL"].append({})
        self.cur.action["EXPEL"][-1]["object"] = object
        self.cur.action["EXPEL"][-1]["container"] = container
        self.cur.empty = False

    def STATECHANGE(self, object, to):
        for thing in [object, to]:
            if thing not in self.cur.containment._graph_dict:
                self.cur.containment.add_object(thing)
                self.cur.space.add_object(thing)
                self.cur.touching.add_object(thing)

        self.cur.action["STATECHANGE"].append({})
        self.cur.action["STATECHANGE"][-1]["object"] = object
        self.cur.action["STATECHANGE"][-1]["to"] = to
        self.cur.empty = False

    def updateACT(self, type: str, key: str, val: str, index=None):
        # get the timestep that needs to be updated
        if not index:
            node = self.cur
        else:
            node = self.get(index)

        # update the last ACT of that type
        node.action[type][-1][key] = val

# # testing
# model = Mental_motion_picture()
# model.PTRANS("elephant", to="home", From="zoo")
# model.PTRANS("bus", to="stop", From="school")
#
# model.advance_time()
# model.PTRANS("rain", to="ground", From="sky")
# model.PSTOP("bus")
# model.PSTOP("elephant")
#
# model.advance_time()
# model.updateACT("PTRANS", "from", "south")
# model.print(1)
# model.print(2)
# model.print(3)
# model.print_latest()

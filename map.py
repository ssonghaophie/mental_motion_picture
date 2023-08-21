"""
Each time_step has three maps stored in it

1. containment map: edge [M, N] means object M contains N

2. spatial map: edge [M, N] means object M is closer to the center
of the planet than object N is (i.e. M is lower than N)

3. touching map: edge [M, N] means object M and N are touching each
other at that particular time_step

Each method that adds an edge to a map should also have a 
corresponding x_method that removes an edge from the map. For example,
contain() adds an edge to the containment map and x_contain() removes
an edge from the containment map.
"""

from graph import Graph


class Containment(Graph):
    """A simple graph class that represents containment relationship
    """

    def contain(self, edge: [str]):
        """ edge is an array like (obj1, obj2)
            in this case, obj1 contains obj2
        """
        obj0, obj1 = self.noun_dict[edge[0]], self.noun_dict[edge[1]]
        self.graph_dict[obj0].append(obj1)

    def x_contain(self, edge: [str]):
        """edge[0] no longer contains edge[1]
        """
        obj0, obj1 = self.noun_dict[edge[0]], self.noun_dict[edge[1]]
        self.graph_dict[obj0].remove(obj1)

    def copy(self):
        new_graph_dict = self.graph_dict.copy()
        new_noun_dict = self.noun_dict.copy()
        return Containment(new_graph_dict, new_noun_dict)


# todo: update to "Position" map
class Space(Graph):
    """A simple graph class that represents spatial relationship
    """

    def under(self, edge: [str]):
        """ edge is a tuple like (obj0, obj1)
            in this case, obj0 is under obj1
        """
        obj0, obj1 = self.noun_dict[edge[0]], self.noun_dict[edge[1]]
        self.graph_dict[obj0].append(obj1)

    def x_under(self, edge: [str]):
        """edge[0] is no longer under edge[1]
        """
        obj0, obj1 = self.noun_dict[edge[0]], self.noun_dict[edge[1]]
        self.graph_dict[obj0].remove(obj1)

    def above(self, edge: [str]):
        """ edge is a tuple like (obj0, obj1)
            in this case, obj0 is above obj1, so obj1 is under obj0
        """
        obj0, obj1 = self.noun_dict[edge[0]], self.noun_dict[edge[1]]
        self.graph_dict[obj1].append(obj0)

    def x_above(self, edge: [str]):
        """edge[0] is no longer above edge[1]
        """
        obj0, obj1 = self.noun_dict[edge[0]], self.noun_dict[edge[1]]
        self.graph_dict[obj1].remove(obj0)

    def copy(self):
        new_graph_dict = self.graph_dict.copy()
        new_noun_dict = self.noun_dict.copy()
        return Space(new_graph_dict, new_noun_dict)


# todo: update to "Contact" map
class Touching(Graph):
    """A simple graph class that represents touching relationship
    """

    def touch(self, edge: [str]):
        """ edge is a tuple like (obj1, obj2)
            in this case, obj1 and obj2 are touching each other
        """
        self.connect([self.noun_dict[edge[0]], self.noun_dict[edge[1]]])

    def x_touch(self, edge: [str]):
        """edge[0] no longer contains edge[1]
        """
        obj0, obj1 = self.noun_dict[edge[0]], self.noun_dict[edge[1]]
        self.graph_dict[obj0].remove(obj1)
        self.graph_dict[obj1].remove(obj0)

    def copy(self):
        new_graph_dict = self.graph_dict.copy()
        new_noun_dict = self.noun_dict.copy()
        return Touching(new_graph_dict, new_noun_dict)

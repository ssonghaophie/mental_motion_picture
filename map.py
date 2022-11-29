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

    def contain(self, edge):
        """ edge is a tuple like (obj1, obj2)
            in this case, obj1 contains obj2
        """
        if edge[0] in self._graph_dict:
            self._graph_dict[edge[0]].append(edge[1])
        else:
            self._graph_dict[edge[0]] = [edge[1]]

    def x_contain(self, edge):
        """edge[0] no longer contains edge[1]
        """
        self._graph_dict[edge[0]].remove(edge[1])

    def copy(self):
        new_dict = self._graph_dict.copy()
        return Containment(new_dict)


class Space(Graph):
    """A simple graph class that represents spatial relationship
    """

    def under(self, edge):
        """ edge is a tuple like (obj0, obj1)
            in this case, obj0 is under obj1
        """
        if edge[0] in self._graph_dict:
            self._graph_dict[edge[0]].append(edge[1])
        else:
            self._graph_dict[edge[0]] = [edge[1]]

    def x_under(self, edge):
        """edge[0] is no longer under edge[1]
        """
        self._graph_dict[edge[0]].remove(edge[1])

    def above(self, edge):
        """ edge is a tuple like (obj0, obj1)
            in this case, obj0 is above obj1, so obj1 is under obj0
        """
        if edge[1] in self._graph_dict:
            self._graph_dict[edge[1]].append(edge[0])
        else:
            self._graph_dict[edge[1]] = [edge[0]]

    def x_above(self, edge):
        """edge[0] is no longer above edge[1]
        """
        self._graph_dict[edge[1]].remove(edge[0])

    def copy(self):
        new_dict = self._graph_dict.copy()
        return Space(new_dict)


class Touching(Graph):
    """A simple graph class that represents touching relationship
    """

    def touch(self, edge):
        """ edge is a tuple like (obj1, obj2)
            in this case, obj1 and obj2 are touching each other
        """
        self.connect(edge)

    def x_touch(self, edge):
        """edge[0] no longer contains edge[1]
        """
        self._graph_dict[edge[0]].remove(edge[1])
        self._graph_dict[edge[1]].remove(edge[0])

    def copy(self):
        new_dict = self._graph_dict.copy()
        return Touching(new_dict)

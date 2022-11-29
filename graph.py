"""
The Graph class is adapted from
https://www.python-course.eu/graphs_python.php
"""


class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict is None:
            graph_dict = {}
        self._graph_dict = graph_dict

    def edges(self, object):
        """ returns a list of all the edges of a vertices"""
        return self._graph_dict[object]

    def all_edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def all_objects(self):
        """ returns the vertices of a graph as a set """
        return set(self._graph_dict.keys())

    def add_object(self, object):
        """ If the object "object" is not in
            self._graph_dict, a key "object" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if object not in self._graph_dict:
            self._graph_dict[object] = []

    def connect(self, edge):
        """ connect two objects with a reflexive edge;
            edge is of type tuple, like (obj1, obj2);
        """
        edge = set(edge)
        obj1, obj2 = tuple(edge)
        for x, y in [(obj1, obj2), (obj2, obj1)]:
            if x in self._graph_dict:
                self._graph_dict[x].append(y)
            else:
                self._graph_dict[x] = [y]

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for object in self._graph_dict:
            for neighbour in self._graph_dict[object]:
                if (neighbour, object) not in edges:
                    edges.append((object, neighbour))
        return edges

    def __iter__(self):
        self._iter_obj = iter(self._graph_dict)
        return self._iter_obj

    def __next__(self):
        """ allows us to iterate over the vertices """
        return next(self._iter_obj)

    def __str__(self):
        res = "objects: "
        for k in self._graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

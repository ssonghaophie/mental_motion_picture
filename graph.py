"""
The Graph class is adapted from
https://www.python-course.eu/graphs_python.php
"""
from noun_phrase import NounPhrase


class Graph(object):

    def __init__(self, graph_dict=None, noun_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if not graph_dict:
            graph_dict = {}
            noun_dict = {}
        self.graph_dict = graph_dict
        self.noun_dict = noun_dict

    def edges(self, obj: NounPhrase):
        """ returns a list of all the edges of a vertex """
        return self.graph_dict[obj]

    def all_edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def all_objects(self):
        """ returns the vertices of a graph as a set """
        return set(self.graph_dict.keys())

    def add_object(self, obj: NounPhrase):
        """ If the object "object" is not in
            self._graph_dict, a key "object" with an empty
            list as a value is added to the dictionary.
            Otherwise, nothing has to be done.
        """
        if obj.noun not in self.noun_dict:
            self.noun_dict[obj.noun] = obj
            self.graph_dict[obj] = []
        else:
            print("object %s already exists in the graph" % obj.noun)

    def connect(self, edge: [NounPhrase]):
        """ connect two objects with a reflexive edge;
            edge is of type tuple, like (obj1, obj2);
        """
        edge = set(edge)
        obj1, obj2 = tuple(edge)
        for x, y in [(obj1, obj2), (obj2, obj1)]:
            if x in self.graph_dict:
                self.graph_dict[x].append(y)
            else:
                self.graph_dict[x] = [y]

    def copy(self):
        new_graph_dict = self.graph_dict.copy()
        new_noun_dict = self.noun_dict.copy()
        return Graph(new_graph_dict, new_noun_dict)

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for obj in self.graph_dict:
            for neighbour in self.graph_dict[obj]:
                if (neighbour, obj) not in edges:
                    edges.append((obj, neighbour))
        return edges

    def __iter__(self):
        self._iter_obj = iter(self.graph_dict)
        return self._iter_obj

    def __next__(self):
        """ allows us to iterate over the vertices """
        return next(self._iter_obj)

    def __str__(self):
        res = "objects: "
        for k in self.noun_dict:
            res += str(self.noun_dict[k]) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += "(" + edge[0].noun + " " + edge[1].noun + ") "
        return res

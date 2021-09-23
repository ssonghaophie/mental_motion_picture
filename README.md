
##### Table of Content

1. [Introduction](#intro)
2. [Structure of the `Mental_model`](#mentalmodel)
3. [Mental Maps](#the-mental-maps)
   1. [The containment map](#the-containment-map)
   2. [The space map](#the-space-map)
   3. [The touching map](#the-touching-map)
4. [The Lexicon](#the-lexicon)
5. [How Does It Work](#how-it-works)
6. [An Example](#example)


## Introduction <a name="intro"> </a>

The purpose of a `Mental_model` is to track when and how objects enter/leave the story, transform into another object, interact with each other, and so on as a short simple story progresses along the timeline, as well as record all primitive acts happened in the story. Provided a lexicon, a mental model analyzes each word in the text according to the entry of the word in the lexicon. Analysis is printed to standard output as a word being analyzed. After the analysis is done, all primitive acts (with respective parameters) happened in the story will also be printed to the standard output. Users can also access incidents and primitive acts happened at a particular `Time_step` on the timeline by specifying the index of that `Time_step`.

## Structure of the `Mental_model` <a name="mentalmodel"></a>

A `Mental_model` is a singly linked-list where each node is a `Time_step` object. For each `Mental_model`, there is a pointer pointing to the most recent `Time_step`. In order record as much information as possible, a mental model writes incidents and primitive acts to the most recent `Time_step` and then the pointer moves to the next `Time_step` as the story progresses. We can think of a `Mental_model` as a timeline, where we record activities happened in a moment and move to the next moment when we are done collecting information about the current moment.

Each `Time_step` consists of three mental maps that help describe incidents happend in that specific timestep: a `containment` map, a `space` map, and a `touching` map.

## Mental Maps <a name="#the-mental-maps"> </a>

In a `Time_step`, each map is a graph object where vertices are objects that appear in the story and edges between vertices indicate connections between objects. We try to depict three different kinds of connection or relationship between physical objects using the `containment` map, the `space` map, and the `touching` map.

### The `containment` map

The containment map aims to depict containment relationships between object. When object B goes inside of object A, we say that A contains B. A real world example would be this: a pen is put into a pencil case, so we say that the pencil case now contains the pen.

A containment relationship is directed and must not go both ways. In other words, if A contains B, then we know for sure that B does not contain A. In this case, an edge `[A, B]` means object A contains object B.

### The `space` map

The goal of the space map is to record the position of an object with respect to the center of earth. In Other words, the closer the object is to the center of earth, the lower the altitude of an object.

Again, the spatial relationship between objects is directed. For the two physical objects A and B, we decide that A can either be above B or below, but not both. An edge in the `space` map must be directed as well. We define that an edge `[A, B]` in a `space` map means object A is closer to the center of the planet than object B is (i.e. M is lower than N).

### The `touching` map

The touching map records if two objects involved in the story are touching one another. A touching relationship is undirected, meaning that if A touched B, B must also touches A. Therefore, edges in the touching map are undirected. An edge `[A, B]` means that these two objects A and B are touching each other.


All three maps must exist in any `Time_step`. If a new physical object appears in the story, the object will be added to all three maps. However, in terms of edges, the three maps are independent of each other. For example, if a containment relationship changes between two object, an edge will be removed to added to the `containment` map, but both `space` map and `touching` map will be unaffected. There may be cases where a new edge is added to more than one map at once, but we still treat maps and edges independently.

## The Lexicon <a name="#the-lexicon"> </a>

A lexicon is a Python dictionary object. As its name indicates, the analyzer goes to the lexicon to find instruction on how to process each word. Each word entry in the lexicon is a `key: value` pair, where the `key` is the word as a string in all uppercase and `value` is the corresponding word `Packet`.

## How Does the Analyzer Work <a name="#how-the-mental_model-works"> </a>


##### Table of Content

1. [Introduction](#intro)
2. [Structure of the `Mental_model`](#mentalmodel)
3. [Mental Maps](#the-mental-maps)
   1. [The containment map](#the-containment-map)
   2. [The space map](#the-space-map)
   3. [The touching map](#the-touching-map)
4. [The Lexicon](#the-lexicon)
5. [How Does the Mental Model Work](#how-it-works)
6. [An Example](#example)
7. [Contrasting ELI and the Mental Model](#contrast)
   1. complex spatial relationship (containment, touching)
   2. the Mental Model is "global" while ELI is not
   3. more primitive acts (STATECHANGE, PSTOP)
   4. decompose more
   5. time_step: inheritance, timespan of an ACT
   6. time_step: order of ACTs
   7. 


## Introduction <a name="intro"> </a>

_Conceptual Dependency(CD) theory, introduced by Roger Schank, is a way to represent meaning of natural language (cite). Conceptual analysis is the act of processing a natural language utterance and creating a non-linguistic ‘picture’ for the meaning of the utterance. Conceptual analyzers like the English Language Interpreter(ELI) (cite) worked by instantiating CD structures corresponding to words in the input. Certain CD structures had “gaps” which are filled in by other CD structures created in the process._

_The original ELI is written in the Common Lisp language. We now have a modified version of ELI written in Python. Besides, we have created a `Mental_model` which can help us preserve more details in analyzing/representing the input utterance._ The purpose of a `Mental_model` is to track when and how objects enter/leave the story, transform into another object, interact with each other, and so on as a short simple story progresses along the timeline, as well as record all primitive acts happened in the story. Provided a lexicon, a mental model analyzes each word in the text according to the entry of the word in the lexicon. Analysis is printed to standard output as a word being analyzed. After the analysis is done, all primitive acts (with respective parameters) happened in the story will also be printed to the standard output. Users can also access incidents and primitive acts happened at a particular `Time_step` on the timeline by specifying the index of that `Time_step`.

## Structure of the `Mental_model` <a name="mentalmodel"></a>

A `Mental_model` is a singly linked-list where each node is a `Time_step` object. For each `Mental_model`, there is a pointer pointing to the most recent `Time_step`. In order record as much information as possible, a mental model writes incidents and primitive acts to the most recent `Time_step` and then the pointer moves to the next `Time_step` as the story progresses. We can think of a `Mental_model` as a timeline, where we record activities happened in a moment and move to the next moment when we are done collecting information about the current moment.

Each `Time_step` consists of three mental maps that help describe incidents happened in that specific `Time_step`: a `containment` map, a `space` map, and a `touching` map.

## Mental Maps <a name="the-mental-maps"> </a>

In a `Time_step`, each map is a graph object where vertices are objects that appear in the story and edges between vertices indicate connections between objects. We try to depict three different kinds of connection or relationship between physical objects using the `containment` map, the `space` map, and the `touching` map.

### The `containment` map <a name="the-containment-map"> </a>

The containment map aims to depict containment relationships between object. When object B goes inside of object A, we say that A contains B. A real world example would be this: a pen is put into a pencil case, so we say that the pencil case now contains the pen.

A containment relationship is directed and must not go both ways. In other words, if A contains B, then we know for sure that B does not contain A. In this case, an edge `[A, B]` means object A contains object B.

### The `space` map <a name="the-space-map"> </a>

The goal of the space map is to record the position of an object with respect to the center of earth. In Other words, the closer the object is to the center of earth, the lower the altitude of an object.

Again, the spatial relationship between objects is directed. For the two physical objects A and B, we decide that A can either be above B or below, but not both. An edge in the `space` map must be directed as well. We define that an edge `[A, B]` in a `space` map means object A is closer to the center of the planet than object B is (i.e. M is lower than N).

### The `touching` map <a name="the-touching-map"> </a>

The touching map records if two objects involved in the story are touching one another. A touching relationship is undirected, meaning that if A touched B, B must also touches A. Therefore, edges in the touching map are undirected. An edge `[A, B]` means that these two objects A and B are touching each other.


All three maps must exist in any `Time_step`. If a new physical object appears in the story, the object will be added to all three maps. However, in terms of edges, the three maps are independent of each other. For example, if a containment relationship changes between two object, an edge will be removed or added to the `containment` map, but both `space` map and `touching` map should be unaffected. There may be cases where a new edge is added to more than one map at once, but we still treat maps and edges independently. _Besides, a `Time_step` is capable of inheriting objects, edges, and primitive ACTs from the `Time_step` precedes it. Unless a physical object transforms into another object, gets destroyed, or disappears from the world of the story in the timespan of the current `Time_step`, it will be copied from to the next `Time_step`. The same principle applies to primitive ACTs and edges in the three maps as well._ 

## The Lexicon <a name="the-lexicon"> </a>

A lexicon is a Python dictionary object. As its name indicates, the analyzer goes to the lexicon to find instruction on how to process each word. Each entry in the lexicon is a `key: value` pair, where the `key` is the word as a string in all uppercase and `value` is the corresponding word `Packet`.

## How Does the Mental Model Work <a name="how-it-works"> </a>



## An Example <a name="example"> </a>



## Contrasting ELI and the Mental Model <a name="contrast"> </a>

How is the Mental Model different from ELI?

### 1. complex spatial relationship

- containment:
- touching:
- ELI's capability?

### 2. the Mental Model is "global" while ELI is not

### 3. more primitive acts (STATECHANGE, PSTOP)

- PSTOP: prepositional phrases help decide when to use PSTOP. When we see fall "on" or stop "at"
- STATECHANGE: one object leave the world and another enters

### 4. support more detail - merge with discussion about time_step

- direction of moving
- 

### 5. time_step: inheritance, timespan of an ACT



### 6. time_step: order of ACTs


  
  
<p>&nbsp;</p>

What we've discussed...

09/29

- Mental model is "Global"
- In ELI you read in a verb, then you instantiate a CD structure with gaps in it and the gaps are going to be filled in by other concepts/physical objects that are in the working memory. For example (Mary picks up a ball), if you read in a verb(pick) and create a PTRANS, you will create subject/object gaps that will be filled in by physical objects(Mary and ball). At the end of it, the physical objects are inside of this complex CD structure. To be able to reason about things happned to the physical objects, you need to go inside of the PTRANS to realize there is a ball or a Mary in the World. With our mental model, we can go to the mental model and and print out the log to see there is a ball/Mary in the world. It will be easier to reason about things happened, especially about the relative location of objects. You don't have to go to the inside of a CD structure and everything is accessible.
- Example: Mary went to the store. After analysis, a PTRANS with an actor gap and an object gap will be initialized and filled in. In this case, the verb "went" initializes the CD sctructure,　"Mary" is used to fill the actor gap and store is used to fill the object gap. Up to this part, both ELI and the mental model behave mainly the same, cause we basically copied this logic from ELI to our mental model. However, if you read in a second sentence "there was a book in the store," the two analyzers will behave differently. ELI has to go back to the PTRANS from the previous sentence to find out that there was a store involved in the PTRANS. ELI then changes things so that the store will also be involved in the CD structures generated by the secend sentence. After reading two sentence, there will be two CD Structures that both have a store involved in it, but it is not obvious that they are the same store. However, for our Mental Model, when we first encounter the "store," we treat it as an physical object, and no mather how many CD structures the object is involved in, the Mental Model knows they're the same store.

<p>&nbsp;</p>

- our Mental Model decomposes things more / higher levels of detail.
- 

<p>&nbsp;</p>

10/04

- to put into the discussion
- the "common knowledge" an analyzer needs to understand the sentence better

<p>&nbsp;</p>

- nonphysical objects treated as objects in our system
- e.g. light, signal, heat, cold

<p>&nbsp;</p>

10/06

- keep stack
- From the stand point of parsing the language, our Mental Model system is built on top of ELI. The request and word packet parts are analogous to the way ELI works. Enhancements we've made to ELI:
- The keep_stack functionality. Certains word packets will stay on the stack (which help us understand structures with multiple prepositional phrases). The keep-stack functionality is also analogous to the "demon" functionality of Dypar. The word packet that has the "keep" flag set to true can remain on the the stack and "fire" multiple times, whereas in ELI, a packet gets removed from the stack as soon as the request of that stack is triggered. Our Mental Model system sort of combines features of both ELI and Dypar.
  
<p>&nbsp;</p>

- update

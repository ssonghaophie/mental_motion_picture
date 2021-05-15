# mental_map

A `Mental_model` is a linked-list where each node is a `Time_step` object. Each `Time_step` has four components: a `containment` map, a `space` map, a `touching` map, and a list of all primitive events happened at this `Time_step`.

A `Mental_map` keeps track of

1. how objects flow in and out of the world.
2. how relationships between objects change. What contains what? What is above what? What is toucing what?
3. what primitive events happen at which `time_step`.
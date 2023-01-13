from mental_model import *

model = MentalMotionPicture()

# 0
# Limestone lies under the soil.
model.add_to_graph("limestone")
model.add_to_graph("soil")
model.under(["limestone", "soil"])
model.touch(["limestone", "soil"])

# 1
# Rain picks up carbon dioxide as it falls to earth.
model.advance_time()
model.add_to_graph("rain")
model.add_to_graph("limestone")
model.add_to_graph("carbon-dioxide")
model.add_to_graph("earth")
model.contain(["rain", "carbon-dioxide"])
model.INGEST(obj="carbon-dioxide", container="rain")
model.PTRANS("carbon-dioxide", to="earth")

# 2
# The rain falls on the soil over the limestone.
model.advance_time()
model.PSTOP("rain")
model.above(["rain", "soil"])
model.add_to_graph("limestone")

# 3
# The carbon dioxide in the rain washes through the soil.
model.advance_time()
model.PTRANS("carbon-dioxide")

# 4
# The carbon dioxide turns into acid.
model.advance_time()
model.STATECHANGE("carbon-dioxide", "acid")

# test print combo
model.add_to_graph("carbon")
model.add_to_graph("dioxide")
combo = [model.cur.space.noun_dict["carbon"], model.cur.space.noun_dict["dioxide"]]
model.cur.space.noun_dict["carbon-dioxide"].combo = combo

model.print_latest()

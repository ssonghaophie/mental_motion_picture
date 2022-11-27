from mental_model import *

model = Mental_motion_picture(Containment(), Space(), Touching())

# 0
# Limestone lies under the soil.
model.under(("limestone", "soil"))
model.touch(("limestone", "soil"))

# 1
# Rain picks up carbon dioxide as it falls to earth.
model.advance_time()
model.contain(("rain", "carbon-dioxide"))
model.INGEST(object="carbon-dioxide", container="rain")
model.PTRANS("carbon-dioxide", to="earth")

# 2
# The rain falls on the soil over the limestone.
model.advance_time()
model.PSTOP("rain")
model.above(('rain', 'soil'))
model.add_object("limestone")

# 3
# The carbon dioxide in the rain washes through the soil.
model.advance_time()
model.PTRANS("carbon-dioxide")

# 4
# The carbon dioxide turns into acid.
model.advance_time()
model.STATECHANGE("carbon-dioxide", "acid")

model.print(4)

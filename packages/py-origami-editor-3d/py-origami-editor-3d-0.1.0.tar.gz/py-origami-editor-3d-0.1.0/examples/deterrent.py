# "A deterrent example" example from OrigamiScript manual

import os
from py_origami_editor_3d.origami import Origami
from py_origami_editor_3d.paper_types import SQUARE

fName = os.path.join(os.path.dirname(__file__), os.path.basename(__file__).replace(".py", ".txt"))

origami = Origami()
origami.comment("At times, it is much harder to fold something in OrigamiScript than it is in real life.")
origami.paper(SQUARE)
origami.plane((200, 0), (1, 0, 0)).reflect()
origami.plane((200, 200), (1, 1, 0)).angle(60).rotate()
origami.plane((200, 200), (0, 1, 0)).angle(60).rotate()
origami.plane((200, 200), (-1, 1, 0)).angle(60).rotate()
origami.planeThrough((200, 0), (200, 200), (200, 400)).target(100, 50).reflect()
origami.planeThrough((0, 0), (200, 200), (400, 0)).target(100, 50).reflect()
origami.planeThrough((0, 400), (200, 200), (400, 400)).target(100, 350).reflect()
origami.comment("This was the minimal code required to fold this particular 'rocket'")
origami.save(fName)

# Boat example from OrigamiScript manual

import os
from py_origami_editor_3d.origami import Origami
from py_origami_editor_3d.paper_types import A4

fName = os.path.join(os.path.dirname(__file__), os.path.basename(__file__).replace(".py", ".txt"))

origami = Origami()
origami.comment("Take an A4 sheet of paper:")
origami.paper(A4)
origami.comment("Fold it back at the top and the bottom so that it becomes a square:")
origami.plane((62.15, 0), (-1, 0, 0)).angle(180).rotate()
origami.plane((362.15, 0), (1, 0, 0)).angle(180).rotate()
origami.comment("Fold it in half:")
origami.plane((212.15, 150), (0, 1, 0)).angle(180).rotate()
origami.comment("Fold the upper corners down:")
origami.plane((212.15, 150), (1, 1, 0)).angle(180).rotate()
origami.plane((212.15, 150), (-1, 1, 0)).angle(-180).rotate()
origami.comment("Open it to make it 3D:")
origami.plane((212.15, 150), (1, 0, 0)).angle(45).rotate()
origami.planeThrough((62.15, 0), (212.15, 150), (362.15, 0)).target(212, 75).reflect()
origami.comment("Arrange the flaps:")
origami.planeThrough((62.15, 0), (212.15, 150), (362.15, 0)).target(322, 110).reflect()
origami.planeThrough((62.15, 0), (212.15, 150), (362.15, 0)).target(10, 290).reflect()
origami.planeThrough((62.15, 0), (212.15, 150), (362.15, 0)).target(410, 10).reflect()
origami.comment("Make the sail with a sink fold:")
origami.plane((212.15, 60), (-14.64466, -100, 35.355)).reflect()
origami.comment("Finished.")
origami.save(fName)

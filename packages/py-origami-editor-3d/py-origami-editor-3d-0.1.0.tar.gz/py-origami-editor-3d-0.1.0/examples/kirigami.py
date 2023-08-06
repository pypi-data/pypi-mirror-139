# Kirigami example from OrigamiScript manual

import os
from py_origami_editor_3d.origami import Origami
from py_origami_editor_3d.paper_types import SQUARE

fName = os.path.join(os.path.dirname(__file__), os.path.basename(__file__).replace(".py", ".txt"))

origami = Origami()
origami.comment("A very basic paper flower")
origami.paper(SQUARE)
origami.comment("Fold in half twice:")
origami.plane((200, 200), (1, 0, 0)).reflect()
origami.plane((200, 200), (0, 1, 0)).reflect()
origami.comment("Cut some paper:")
origami.angleBisector((200, 0), (100, 0), (200, 100)).cut()
origami.angleBisector((0, 200), (0, 100), (100, 200)).cut()
origami.plane((130, 200), (1, 1, 0)).cut()
origami.comment("Unfold:")
origami.target(100, 100).plane((200, 200), (1, 0, 0)).reflect()
origami.target(100, 100).plane((200, 200), (0, 1, 0)).reflect()
origami.save(fName)

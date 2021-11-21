from symmetry.groups import GroupAction, GeneratedGroup, MatrixGroupAction

BASE_MATRIX_MAP = {
    "I": (1, 0, 0, 1),
    "Tx": (-1, 0, 0, 1),
    "S": (0, -1, 1, 0),
    "Ty": (1, 0, 0, -1),
    "Txy": (0, 1, 1, 0)
}
MATRIX_NAMES = {
    t: name for name, t in BASE_MATRIX_MAP.items()
}


class PlanarGroupAction(MatrixGroupAction):

    def id(self):
        return self.__class__(BASE_MATRIX_MAP["I"])

    @classmethod
    def rot90(cls):
        return cls(BASE_MATRIX_MAP["S"])

    @classmethod
    def flip_y(cls):
        return cls(BASE_MATRIX_MAP["Ty"])

    @classmethod
    def flip_x(cls):
        return cls(BASE_MATRIX_MAP["Tx"])

    @classmethod
    def swap_xy(cls):
        return cls(BASE_MATRIX_MAP["Txy"])

    @property
    def name(self):
        return MATRIX_NAMES[self.matrix_elements]


Z4_SQUARE = GeneratedGroup({PlanarGroupAction.rot90()})
D4_SQUARE = GeneratedGroup({PlanarGroupAction.rot90(), PlanarGroupAction.flip_x()})

# todo generalize
_s = PlanarGroupAction.rot90()
_t = PlanarGroupAction.flip_x()
for (g1, g2) in ((_s, _s), (_s * _s, _s), (_s, _t), (_s * _s, _t), (_s * _s * _s, _t)):
    MATRIX_NAMES[(g1 * g2).matrix_elements] = f"{g1.name}{g2.name}"

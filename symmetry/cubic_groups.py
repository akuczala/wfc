import numpy as np

from symmetry.groups import GeneratedGroup, MatrixGroupAction

BASE_MATRIX_MAP = {
    name: tuple(int(x) for x in mat.ravel())
    for name, mat in {
        "I": np.eye(3),
        "Tx": np.diag([-1, 1, 1]),
        "Rxy": np.array([
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ]),
        "Rxz": np.array([
            [0, 0, -1],
            [0, 1, 0],
            [1, 0, 0]
        ]),
        "Ryz": np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0]
        ]),
        "Ty": np.diag([1, -1, 1]),
        "Tz": np.diag([1, 1, -1]),
    }.items()
}
MATRIX_NAMES = {
    t: name for name, t in BASE_MATRIX_MAP.items()
}


class CubicGroupAction(MatrixGroupAction):

    def id(self):
        return self.cubic_id()

    @classmethod
    def cubic_id(cls):
        return cls(BASE_MATRIX_MAP["I"])

    @classmethod
    def xy90(cls):
        return cls(BASE_MATRIX_MAP["Rxy"])

    @classmethod
    def xz90(cls):
        return cls(BASE_MATRIX_MAP["Rxz"])

    @classmethod
    def yz90(cls):
        return cls(BASE_MATRIX_MAP["Ryz"])

    @classmethod
    def flip_y(cls):
        return cls(BASE_MATRIX_MAP["Ty"])

    @classmethod
    def flip_x(cls):
        return cls(BASE_MATRIX_MAP["Tx"])

    @classmethod
    def flip_z(cls):
        return cls(BASE_MATRIX_MAP["Tz"])

    @property
    def name(self):
        return MATRIX_NAMES[self.matrix_elements]

    @classmethod
    def swap_xy(cls):
        return cls.xy90() * cls.flip_y()


CUBIC_GROUP = GeneratedGroup({
    CubicGroupAction.xy90(), CubicGroupAction.xz90(), CubicGroupAction.yz90(),
    CubicGroupAction.flip_x()})

D4_SQUARE_Z = GeneratedGroup({
    CubicGroupAction.xy90(), CubicGroupAction.flip_x()
})

for name, g in CUBIC_GROUP.generate_names().items():
    MATRIX_NAMES[g.matrix_elements] = name
pass

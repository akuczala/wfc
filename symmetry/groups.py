from __future__ import annotations

import itertools
from abc import abstractmethod
from dataclasses import dataclass
from functools import reduce

from utils import signed_permutation_inverse_2x2
from typing import Set, Tuple, Dict

import numpy as np


class GroupTargetMixin:
    @abstractmethod
    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        pass

    def generate_from_group(self, group: Group) -> Dict[GroupAction, GroupTargetMixin]:
        # cannot get unique members with a dict/set since we aren't guaranteed to be hashable (and doing so is annoying)
        # must check explicitly
        out = {}
        for g in group.get_elements():
            target = self.transform(g)
            if target not in out.values():
                out[g] = target
        return out


class TrivialGroupTarget(GroupTargetMixin):

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return self

    def __eq__(self, other):
        return isinstance(other, TrivialGroupTarget)

    def __hash__(self):
        return hash(TrivialGroupTarget)


class GroupAction:
    matrix_elements: Tuple[int, int, int, int]

    @abstractmethod
    def id(self):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def inverse(self):
        pass

    @abstractmethod
    def power_iterator(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass


# Integer Matrices only
@dataclass(frozen=True)
class MatrixGroupAction(GroupAction):
    matrix_elements: Tuple[int, ...]

    def id(self):
        return np.eye(self.dim)

    @property
    def dim(self) -> int:
        return int(np.sqrt(len(self.matrix_elements)))

    @classmethod
    def from_matrix(cls, matrix: np.ndarray):
        assert matrix.dtype == np.int
        assert matrix.shape[0] == matrix.shape[1]
        return cls(
            matrix_elements=tuple(x for x in matrix.ravel())
        )

    @property
    def matrix(self) -> np.ndarray:
        return np.array(self.matrix_elements).reshape(self.dim, self.dim)

    def __mul__(self, other):
        return self.from_matrix(np.dot(self.matrix, other.matrix))

    def inverse(self):
        return self.from_matrix(signed_permutation_inverse_2x2(self.matrix))

    def power_iterator(self):
        def power_generator(a):
            yield self.id()
            g = a
            while g != self.id():
                yield g
                g = g * a

        return iter(power_generator(self))

    def __eq__(self, other):
        return self.matrix_elements == other.matrix_elements

    def __hash__(self):
        return self.matrix_elements.__hash__()


class Group:

    @abstractmethod
    def id(self) -> GroupAction:
        pass

    def get_elements(self) -> Set[GroupAction]:
        pass

    def __len__(self):
        return len(self.get_elements())


# todo: give this an identity element somehow
@dataclass
class GeneratedGroup(Group):
    generators: Set[GroupAction]

    def id(self) -> GroupAction:
        return next(iter(self.generators)).id()

    def get_elements(self) -> Set[GroupAction]:
        return {
            reduce(lambda g1, g2: g1 * g2, g_tuple)
            for g_tuple in itertools.product(*(gen.power_iterator() for gen in self.generators))
        }

    def generate_names(self) -> Dict[str, GroupAction]:
        out = {g.name: g for g in self.generators}
        out[self.id().name] = self.id()
        # if we use a list of generators rather than list of lists, the generators do not each
        # capture their appropriate value of gen
        name_g_pair_gens = [
            [(self._name_generator_power(gen, p), g) for p, g in enumerate(gen.power_iterator())]
            for gen in self.generators
        ]
        for pairs in itertools.product(*name_g_pair_gens):
            names, group_elements = zip(*pairs)
            g = reduce(lambda g1, g2: g1 * g2, group_elements)
            if g not in out.values():
                out["".join((n for n in names if n != self.id().name))] = g
        return out

    def _name_generator_power(self, gen: GroupAction, p: int) -> str:
        if p == 0:
            return self.id().name
        if p == 1:
            return gen.name
        return f"{gen.name}^{p}_"


@dataclass
class Trivial(Group):
    _id: GroupAction

    def id(self) -> GroupAction:
        return self._id

    def get_elements(self) -> Set[GroupAction]:
        return {self.id()}

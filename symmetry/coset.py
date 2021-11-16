from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Set

from symmetry.groups import GroupAction, Group, GroupTargetMixin


class GroupCoset(GroupTargetMixin, frozenset):

    @classmethod
    def from_group(cls, group: Group):
        return cls(group.get_elements())

    @classmethod
    def partition_group(cls, group: Group, stabilizer_group: Group) -> Set[GroupCoset]:
        stabilizer_coset = cls.from_group(stabilizer_group)
        return {stabilizer_coset.left_action(g) for g in group.get_elements()}

    def left_action(self, g: GroupAction):
        return GroupCoset(g * h for h in self)

    def conjugate(self, g: GroupAction):
        return GroupCoset(g * h * g.inverse() for h in self)

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return self.left_action(g_action)
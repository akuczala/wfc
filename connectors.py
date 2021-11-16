from abc import ABC, abstractmethod
from dataclasses import dataclass

from symmetry.coset import GroupTargetMixin
from symmetry.groups import GroupAction


class Connectors(ABC):
    @abstractmethod
    def transform(self, g_action: GroupAction):
        pass


class ProtoConnectors(ABC):
    pass


@dataclass
class GeneratedConnector(GroupTargetMixin):
    proto_connector: ProtoConnectors
    g_target: GroupTargetMixin

    def transform(self, g_action: GroupAction):
        return GeneratedConnector(self.proto_connector, self.g_target.transform(g_action))
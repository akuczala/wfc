from abc import ABC, abstractmethod
from dataclasses import dataclass


class Connectors(ABC):
    @abstractmethod
    def transform(self, g_action: "GroupAction"):
        pass


class ProtoConnectors(ABC):
    pass


@dataclass
class GeneratedConnector:
    proto_connector: ProtoConnectors
    g_action: "GroupAction"

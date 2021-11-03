from abc import ABC, abstractmethod


class Connectors(ABC):
    @abstractmethod
    def transform(self, g_action: "GroupAction"):
        pass

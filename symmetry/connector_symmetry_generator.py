from typing import Dict, Optional

from connectors import ProtoConnectors, Connectors, GeneratedConnector
from symmetry.coset import GroupCoset
from symmetry.groups import Group, TrivialGroupTarget


class ConnectorSymmetryGenerator:
    def __init__(self, symmetry_dict: Dict[ProtoConnectors, Optional[Group]]):
        self.symmetry_dict = symmetry_dict

    def make_base_connector_dict(self) -> Dict[ProtoConnectors, Connectors]:
        return {
            proto_name: self.make_base_connector(proto_name, group)
            for proto_name, group in self.symmetry_dict.items()
        }

    @staticmethod
    def make_base_connector(name: ProtoConnectors, group: Optional[Group]) -> Connectors:
        if group is None:
            return GeneratedConnector(name, TrivialGroupTarget())
        else:
            return GeneratedConnector(name, GroupCoset.from_group(group))

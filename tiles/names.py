from enum import Enum


class ProtoTileNames(Enum):

    def get_all_tiles(self):
        return {t for t in self}


class TileNames:
    pass
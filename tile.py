import random

class Tile:

    def __init__(self, possible_tiles, pos):
        self.pos = list(pos)
        self.possible_tiles = possible_tiles
        self.collapsed = False
        self.tile_index = -1

    def collapse_tile(self):
        self.tile_index = random.choice(self.possible_tiles)
    
        self.collapsed = True

class Square:

    def __init__(self, surface):
        self.surface = surface


class Block(Square):
    pass


class Exit(Square):
    def __init__(self, surface, value):
        self.surface = surface
        self.value = value


class Spawner(Square):
    pass



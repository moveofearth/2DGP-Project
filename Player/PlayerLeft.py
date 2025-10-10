import Player
from Character import Priest


class PlayerLeft(Player):
    def __init__ (self):
        pass

    def initialize(self):
        self.dir = 1
        self.character = Priest.Priest()
        self.character.initialize()
        pass

    def update(self, deltaTime):
        pass

    def render(self):
        self.character.render()
        pass
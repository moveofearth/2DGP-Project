import pico2d
import pathlib
import Config
from Character import Character

class Player:
    def __init__ (self):
        self.x, self.y = 400, 300
        self.dir = 0 # right -1, left 1
        self.state = 'Idle' # Idle, Walk
        self.character = Character.Character()

    def initialize(self):
        pass

    def update(self, deltaTime):
        pass

    def render(self):
        pass
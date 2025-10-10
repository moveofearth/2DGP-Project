import pico2d
import Priest

class Character:
    def __init__ (self):
        self.image = None
        self.frame = 0
        self.x, self.y = 400, 300


    def initialize(self):
        pass

    def update(self, deltaTime):
        pass

    def render(self):
        self.image.draw(self.x, self.y)
        pass

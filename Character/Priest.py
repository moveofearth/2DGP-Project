import Character
import pathlib

class Priest(Character):
    def __init__(self):
        pass

    def initialize(self):
        path = pathlib.Path.cwd() / 'Resources' / 'Character' / 'Priest' / '0000.png'
        self.image.load_image(str(path))
        pass

    def update(self, deltaTime):
        pass

    def render(self):
        pass
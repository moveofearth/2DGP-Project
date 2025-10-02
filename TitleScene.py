import pico2d
import Config
import pathlib

class TitleScene:
    def __init__(self):
        self.image = None

    def initialize(self):
        path = pathlib.Path.cwd() / 'Resources' / 'Scene' / 'temptitle.png'
        self.image = pico2d.load_image(str(path))
        pass

    def update(self, deltaTime):
        pass

    def render(self):
        self.image.draw(Config.windowWidth // 2, Config.windowHeight // 2)
        pass

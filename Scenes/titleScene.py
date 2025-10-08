import pico2d
import Config  # 기존 그대로
import pathlib

class TitleScene:
    def __init__(self):
        self.image = None
    def initialize(self):
        path = pathlib.Path.cwd() / 'Resources' / 'Scene' / 'title.png'
        self.image = pico2d.load_image(str(path))
    def update(self, deltaTime):
        pass
    def render(self):
        if self.image:
            self.image.draw(Config.windowWidth // 2, Config.windowHeight // 2)
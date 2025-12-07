import pico2d
import config  # 기존 그대로
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
            # 화면 크기에 맞게 스트레치
            self.image.draw(config.windowWidth // 2, config.windowHeight // 2,
                          config.windowWidth, config.windowHeight)

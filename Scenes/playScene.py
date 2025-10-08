import pico2d
import pathlib

class PlayScene:
    def __init__(self):
        self.background = None

    def initialize(self):
        # 플레이 배경 이미지 로딩
        base_path = pathlib.Path.cwd() / 'Resources' / 'Scene'
        self.background = pico2d.load_image(str(base_path / 'stage.png'))

    def update(self, deltaTime):
        pass

    def render(self):
        if self.background:
            self.background.draw(640, 360)  # 화면 중앙에 그리기


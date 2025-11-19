import pico2d
import config  # 기존 그대로
import pathlib

class TitleScene:
    def __init__(self):
        self.background = None

    def initialize(self):
        # 타이틀 배경 이미지 로딩
        base_path = pathlib.Path.cwd() / 'Resources' / 'Scene'
        self.background = pico2d.load_image(str(base_path / 'title.png'))

    def update(self, deltaTime):
        pass

    def render(self):
        if self.background:
            # 배경을 2배 스케일링하여 전체 화면에 맞춤 (960x540 -> 1920x1080)
            self.background.draw(960, 540, self.background.w * 2, self.background.h * 2)

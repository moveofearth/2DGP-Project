from .character import Character  # 기존 그대로
import pathlib
import pico2d


class Priest(Character):

    def __init__(self):
        super().__init__()  # 부모 __init__ 호출 추가
        self.image = None
        self.frame = 0
        self.x, self.y = 400, 300


    def initialize(self):
        pass


    def update(self, deltaTime):
        pass


    def render(self):
        if self.image:
            self.image.draw(self.x, self.y)

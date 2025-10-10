import pico2d


class Character:
    def init (self):
        self.image = None
        self.frame = 0
        self.x, self.y = 400, 300

    def initialize(self):
        pass

    def update(self, deltaTime):
        pass

    def render(self):
        if self.image:  # 이미지 None 체크 추가
            self.image.draw(self.x, self.y)
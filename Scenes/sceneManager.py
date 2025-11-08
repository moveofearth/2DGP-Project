import pico2d


class SceneManager:
    def __init__(self):
        self.background = None

    def initialize(self):
        # 기본 배경 생성 (단색)
        pass

    def render(self):
        # 기본 배경 렌더링 (회색)
        pico2d.clear_canvas()

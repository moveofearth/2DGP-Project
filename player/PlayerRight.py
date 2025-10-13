from .Player import Player


class PlayerRight(Player):
    def __init__(self):
        super().__init__(x=600, y=300)  # 플레이어2는 오른쪽에 위치

    def initialize(self):
        self.dir = 1  # 왼쪽을 바라보도록 1로 설정

    def update(self, deltaTime, input_dir=None):
        super().update(deltaTime, input_dir)

    def render(self):
        pass

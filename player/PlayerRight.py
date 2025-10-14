from .Player import Player


class PlayerRight(Player):
    def __init__(self):
        super().__init__(x=600, y=300)  # 플레이어2는 오른쪽에 위치

    def initialize(self):
        self.dir = 1  # 왼쪽을 바라보도록 1로 설정

    def update(self, deltaTime, input_dir=None):
        if input_dir == 'left':
            self.x -= 3
            self.state = 'Walk'  # 왼쪽으로 갈 때 Walk
        elif input_dir == 'right':
            self.x += 1
            self.state = 'BackWalk'  # 오른쪽으로 갈 때 BackWalk
        elif input_dir == 'fastMiddleATK':
            self.state = 'fastMiddleATK'
        else:
            self.state = 'Idle'  # 입력이 없으면 Idle 상태

    def render(self):
        pass

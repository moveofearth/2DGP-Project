# from character.Priest import Priest  # SpriteManager 사용으로 주석 처리
from .Player import Player  # 같은 디렉터리 상대 import


class PlayerLeft(Player):
    def __init__(self):
        super().__init__()  # 부모 __init__ 호출 추가

    def initialize(self):
        self.dir = -1  # 오른쪽을 바라보도록 -1로 설정

    def update(self, deltaTime, move_input=None, atk_input=None):  # 이동과 공격 입력을 분리
        # 공격 입력 처리 (이동 중에도 가능)
        if atk_input == 'fastMiddleATK' and not self.is_attacking:
            self.state = 'fastMiddleATK'
            self.is_attacking = True
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongMiddleATK' and not self.is_attacking:
            self.state = 'strongMiddleATK'
            self.is_attacking = True
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongUpperATK' and not self.is_attacking:
            self.state = 'strongUpperATK'
            self.is_attacking = True
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongLowerATK' and not self.is_attacking:
            self.state = 'strongLowerATK'
            self.is_attacking = True
            return  # 공격 시작 시 이동은 무시

        # 공격 중이 아닐 때만 이동 처리
        if not self.is_attacking:
            if move_input == 'left':
                self.x -= 1
                self.state = 'BackWalk'  # 왼쪽으로 갈 때 BackWalk
            elif move_input == 'right':
                self.x += 3
                self.state = 'Walk'  # 오른쪽으로 갈 때 Walk
            else:
                self.state = 'Idle'  # 입력이 없으면 Idle 상태

    def render(self):
        pass

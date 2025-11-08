from .player import Player


class PlayerRight(Player):
    def __init__(self):
        super().__init__(x=600, y=300, character_type='priest')  # priest 캐릭터로 초기화

    def initialize(self):
        super().initialize()
        self.dir = 1  # 왼쪽을 바라보도록 1로 설정

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False):
        # 캐릭터 위치 동기화
        self.character.x, self.character.y = self.x, self.y
        self.character.state = self.state

        # Character 업데이트
        self.character.update(deltaTime)

        # 연계 공격 입력 처리
        if combo_input and self.can_combo:
            if (self.get_character_type() == 'priest' and self.state == 'strongMiddleATK') or \
               (self.get_character_type() == 'thief' and self.state in ['fastMiddleATK', 'fastMiddleATK2', 'strongMiddleATK']):
                self.combo_reserved = True
                return

        # 공격 입력 처리 (이동 중에도 가능)
        if atk_input == 'fastMiddleATK' and not self.is_attacking:
            self.state = 'fastMiddleATK'
            self.is_attacking = True
            # thief는 fastMiddleATK에서도 연계 가능
            self.can_combo = True if self.get_character_type() == 'thief' else False
            self.combo_reserved = False
            return
        elif atk_input == 'strongMiddleATK' and not self.is_attacking:
            self.state = 'strongMiddleATK'
            self.is_attacking = True
            # 모든 캐릭터가 strongMiddleATK에서 연계 가능
            self.can_combo = True
            self.combo_reserved = False
            return
        elif atk_input == 'strongUpperATK' and not self.is_attacking:
            self.state = 'strongUpperATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return
        elif atk_input == 'strongLowerATK' and not self.is_attacking:
            self.state = 'strongLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return

        # 공격 중이 아닐 때만 이동 처리
        if not self.is_attacking:
            if move_input == 'left':
                self.x -= 1
                self.state = 'Walk'  # 왼쪽으로 갈 때 Walk
            elif move_input == 'right':
                self.x += 0.5
                self.state = 'BackWalk'  # 오른쪽으로 갈 때 BackWalk
            else:
                self.state = 'Idle'  # 입력이 없으면 Idle 상태

    def render(self):
        super().render()  # Character 렌더링

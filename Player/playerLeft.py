from .player import Player


class PlayerLeft(Player):
    def __init__(self):
        super().__init__(x=600, y=300, character_type='thief')

    def initialize(self):
        super().initialize()
        self.dir = -1  # 오른쪽을 바라보도록 -1로 설정

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False, char_change_input=None):
        # 캐릭터 변경 처리 (공격 중이 아닐 때만)
        if char_change_input and not self.is_attacking:
            self.set_character_type(char_change_input)
            return

        # 캐릭터 위치 동기화
        self.character.x, self.character.y = self.x, self.y
        self.character.state = self.state

        # Character 업데이트
        self.character.update(deltaTime)

        # 연계 공격 입력 처리
        if combo_input and self.can_combo:
            if (self.get_character_type() == 'priest' and self.state == 'strongMiddleATK') or \
               (self.get_character_type() == 'thief' and self.state in ['fastMiddleATK', 'fastMiddleATK2', 'strongMiddleATK', 'strongUpperATK']) or \
               (self.get_character_type() == 'fighter' and self.state in ['fastMiddleATK', 'fastMiddleATK2', 'strongUpperATK']):
                self.combo_reserved = True
                return

        # rage 스킬 입력 처리 (가장 높은 우선순위)
        if atk_input == 'rageSkill' and not self.is_attacking and self.can_use_attack('rageSkill'):
            self.state = 'rageSkill'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return

        # 공격 입력 처리 (이동 중에도 가능) - 캐릭터별 공격 제한 적용
        if atk_input == 'fastMiddleATK' and not self.is_attacking and self.can_use_attack('fastMiddleATK'):
            self.state = 'fastMiddleATK'
            self.is_attacking = True
            # thief와 fighter는 fastMiddleATK에서도 연계 가능
            self.can_combo = True if self.get_character_type() in ['thief', 'fighter'] else False
            self.combo_reserved = False
            return
        elif atk_input == 'fastLowerATK' and not self.is_attacking and self.can_use_attack('fastLowerATK'):
            self.state = 'fastLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return
        elif atk_input == 'fastUpperATK' and not self.is_attacking and self.can_use_attack('fastUpperATK'):
            self.state = 'fastUpperATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return
        elif atk_input == 'strongMiddleATK' and not self.is_attacking and self.can_use_attack('strongMiddleATK'):
            self.state = 'strongMiddleATK'
            self.is_attacking = True
            # 모든 캐릭터가 strongMiddleATK에서 연계 가능
            self.can_combo = True
            self.combo_reserved = False
            return
        elif atk_input == 'strongUpperATK' and not self.is_attacking and self.can_use_attack('strongUpperATK'):
            self.state = 'strongUpperATK'
            self.is_attacking = True
            # thief와 fighter는 strongUpperATK에서도 연계 가능
            self.can_combo = True if self.get_character_type() in ['thief', 'fighter'] else False
            self.combo_reserved = False
            return
        elif atk_input == 'strongLowerATK' and not self.is_attacking and self.can_use_attack('strongLowerATK'):
            self.state = 'strongLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return

        # 공격 중이 아닐 때만 이동 처리 - 캐릭터별 이동속도 적용
        if not self.is_attacking:
            move_speed = self.get_move_speed()
            if move_input == 'left':
                self.x -= move_speed * 0.5 * deltaTime  # 왼쪽은 느리게
                self.state = 'BackWalk'  # 왼쪽으로 갈 때 BackWalk
            elif move_input == 'right':
                self.x += move_speed * deltaTime
                self.state = 'Walk'  # 오른쪽으로 갈 때 Walk
            else:
                self.state = 'Idle'  # 입력이 없으면 Idle 상태

    def render(self):
        super().render()  # 부모의 바운딩 박스 그리기만 호출

    def get_bb(self):
        """바운딩 박스 좌표 반환 - PlayerLeft용 (왼쪽으로 50, 아래로 50 이동)"""
        # 1.5배 스케일링 적용
        bb_width = 40 * 1.5  # 60
        bb_height = 50 * 1.5  # 75
        adjusted_x = self.x - (30 * 1.5)
        adjusted_y = self.y - (50 * 1.5)
        return adjusted_x - bb_width, adjusted_y - bb_height, adjusted_x + bb_width, adjusted_y + bb_height

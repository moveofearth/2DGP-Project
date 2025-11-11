from Character.character import Character


class Player:

    def __init__(self, x=400, y=300, character_type='priest'):
        self.x, self.y = x, y
        self.character = Character(character_type)  # Character 인스턴스 추가
        self.character.x, self.character.y = x, y  # 캐릭터 위치 동기화

        self.dir = -1  # 항상 오른쪽을 바라보도록 -1로 고정
        self.state = 'Idle'  # Idle, Walk, BackWalk
        self.is_attacking = False  # 공격 중인지 체크
        self.can_combo = False  # 연계 가능 상태
        self.combo_reserved = False  # 연계 공격 예약 상태

        # 캐릭터별 사용 가능한 공격 정의
        self.available_attacks = {
            'priest': ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK', 'strongLowerATK', 'rageSkill'],
            'thief': ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK', 'strongLowerATK'],
            'fighter': ['fastMiddleATK', 'fastLowerATK', 'fastUpperATK', 'strongMiddleATK', 'strongLowerATK', 'strongUpperATK']
        }

    def can_use_attack(self, attack_type):
        """현재 캐릭터가 해당 공격을 사용할 수 있는지 확인"""
        character_type = self.get_character_type()
        return attack_type in self.available_attacks.get(character_type, [])

    def is_attack_state(self):
        """현재 상태가 공격 상태인지 확인"""
        attack_states = ['fastMiddleATK', 'fastMiddleATK2', 'fastMiddleATK3', 'strongMiddleATK', 'strongMiddleATK2', 'strongUpperATK', 'strongUpperATK2', 'strongLowerATK', 'fastLowerATK', 'fastUpperATK', 'rageSkill']
        return self.state in attack_states

    def get_move_speed(self):
        """현재 캐릭터의 이동속도 반환"""
        return self.character.get_move_speed()

    def initialize(self):
        self.character.initialize()  # Character 초기화

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False, char_change_input=None):
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
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'fastLowerATK' and not self.is_attacking and self.can_use_attack('fastLowerATK'):
            self.state = 'fastLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'fastUpperATK' and not self.is_attacking and self.can_use_attack('fastUpperATK'):
            self.state = 'fastUpperATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongMiddleATK' and not self.is_attacking and self.can_use_attack('strongMiddleATK'):
            self.state = 'strongMiddleATK'
            self.is_attacking = True
            # 모든 캐릭터가 strongMiddleATK에서 연계 가능
            self.can_combo = True
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongUpperATK' and not self.is_attacking and self.can_use_attack('strongUpperATK'):
            self.state = 'strongUpperATK'
            self.is_attacking = True
            # thief와 fighter는 strongUpperATK에서도 연계 가능
            self.can_combo = True if self.get_character_type() in ['thief', 'fighter'] else False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongLowerATK' and not self.is_attacking and self.can_use_attack('strongLowerATK'):
            self.state = 'strongLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시

        # 공격 중이 아닐 때만 이동 처리
        if not self.is_attacking:
            move_speed = self.get_move_speed()
            if move_input == 'left':
                self.x -= move_speed * deltaTime
                self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
            elif move_input == 'right':
                self.x += move_speed * deltaTime
                self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
            else:
                self.state = 'Idle'  # 입력이 없으면 Idle 상태

    def render(self):
        self.character.render()  # Character 렌더링

    def set_character_type(self, character_type):
        """캐릭터 타입 변경"""
        self.character.set_character_type(character_type)

    def get_character_type(self):
        """현재 캐릭터 타입 반환"""
        return self.character.get_character_type()

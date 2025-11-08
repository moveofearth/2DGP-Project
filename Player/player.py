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

    def is_attack_state(self):
        """현재 상태가 공격 상태인지 확인"""
        attack_states = ['fastMiddleATK', 'fastMiddleATK2', 'fastMiddleATK3', 'strongMiddleATK', 'strongMiddleATK2', 'strongUpperATK', 'strongLowerATK']
        return self.state in attack_states

    def initialize(self):
        self.character.initialize()  # Character 초기화

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False):
        # 캐릭터 위치 동기화
        self.character.x, self.character.y = self.x, self.y
        self.character.state = self.state

        # Character 업데이트
        self.character.update(deltaTime)

        # 연계 공격 입력을 받으면 예약 상태로 설정 (즉시 전환하지 않음)
        if combo_input and self.state == 'strongMiddleATK' and self.can_combo:
            self.combo_reserved = True
            return

        # 공격 입력 처리 (이동 중에도 가능)
        if atk_input == 'fastMiddleATK' and not self.is_attacking:
            self.state = 'fastMiddleATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongMiddleATK' and not self.is_attacking:
            self.state = 'strongMiddleATK'
            self.is_attacking = True
            self.can_combo = True  # strongMiddleATK는 연계 가능
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongUpperATK' and not self.is_attacking:
            self.state = 'strongUpperATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongLowerATK' and not self.is_attacking:
            self.state = 'strongLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시

        # 공격 중이 아닐 때만 이동 처리
        if not self.is_attacking:
            if move_input == 'left':
                self.x -= 1
                self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
            elif move_input == 'right':
                self.x += 1
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

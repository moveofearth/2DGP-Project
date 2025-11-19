import pico2d
import pathlib
import config


class Character:
    def __init__(self, character_type='priest'):
        self.currentCharacter = character_type  # 현재 캐릭터 타입
        self.image = None
        self.frame = 0
        self.x, self.y = 400, config.GROUND_Y  # 그라운드에 위치
        self.state = 'Idle'
        self.hp = 100  # HP 추가
        self.max_hp = 100  # 최대 HP 추가

        # 물리 변수 추가
        self.velocity_y = 0.0
        self.is_grounded = True

        # 캐릭터별 이동속도 설정
        self.move_speeds = {
            'priest': 250.0,
            'thief': 300.0,
            'fighter': 300.0
        }

    def initialize(self):
        # 캐릭터 타입에 따른 초기화
        if self.currentCharacter in ['priest', 'thief', 'fighter']:
            self._initialize_character()

    def _initialize_character(self):
        """모든 캐릭터 공통 초기화"""
        # 캐릭터 전용 초기화 로직
        pass

    def update(self, deltaTime):
        # 캐릭터 타입에 따른 업데이트
        if self.currentCharacter in ['priest', 'thief', 'fighter']:
            self._update_character(deltaTime)

    def _update_character(self, deltaTime):
        """모든 캐릭터 공통 업데이트"""
        # 캐릭터 전용 업데이트 로직
        pass

    def render(self):
        if self.image:  # 이미지 None 체크 추가
            self.image.draw(self.x, self.y)

    def set_character_type(self, character_type):
        """캐릭터 타입 변경"""
        if character_type in ['priest', 'thief', 'fighter']:
            self.currentCharacter = character_type
            self.initialize()  # 새 캐릭터로 초기화

    def get_character_type(self):
        """현재 캐릭터 타입 반환"""
        return self.currentCharacter

    def get_move_speed(self):
        """현재 캐릭터의 이동속도 반환"""
        return self.move_speeds.get(self.currentCharacter, 200.0)

    def take_damage(self, damage):
        """데미지를 받는 메서드"""
        self.hp = max(0, self.hp - damage)
        return self.hp

    def heal(self, amount):
        """체력을 회복하는 메서드"""
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp

    def is_alive(self):
        """생존 여부 확인"""
        return self.hp > 0

    def get_hp_percentage(self):
        """HP 퍼센테이지 반환 (0.0 ~ 1.0)"""
        return self.hp / self.max_hp if self.max_hp > 0 else 0.0


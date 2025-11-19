import pico2d
import pathlib


class Character:
    def __init__(self, character_type='priest'):
        self.currentCharacter = character_type  # 현재 캐릭터 타입
        self.image = None
        self.frame = 0
        self.x, self.y = 400, 300
        self.state = 'Idle'

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
        self.currentCharacter = character_type
        self.initialize()  # 새 캐릭터로 초기화

    def get_character_type(self):
        """현재 캐릭터 타입 반환"""
        return self.currentCharacter

    def get_move_speed(self):
        """현재 캐릭터의 이동속도 반환"""
        return self.move_speeds.get(self.currentCharacter, 200.0)

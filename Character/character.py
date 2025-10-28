import pico2d
import pathlib


class Character:
    def __init__(self, character_type='priest'):
        self.currentCharacter = character_type  # 현재 캐릭터 타입
        self.image = None
        self.frame = 0
        self.x, self.y = 400, 300
        self.state = 'Idle'

    def initialize(self):
        # 캐릭터 타입에 따른 초기화
        if self.currentCharacter == 'priest' or self.currentCharacter == 'thief':
            # thief는 priest와 같은 초기화 로직 사용
            self._initialize_priest()

    def _initialize_priest(self):
        """Priest 캐릭터 초기화"""
        # Priest 전용 초기화 로직
        pass

    def update(self, deltaTime):
        # 캐릭터 타입에 따른 업데이트
        if self.currentCharacter == 'priest' or self.currentCharacter == 'thief':
            # thief는 priest와 같은 업데이트 로직 사용
            self._update_priest(deltaTime)

    def _update_priest(self, deltaTime):
        """Priest 캐릭터 업데이트"""
        # Priest 전용 업데이트 로직
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

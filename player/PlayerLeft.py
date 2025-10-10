from character.Priest import Priest  # import 수정: 패키지.모듈 import 클래스
from .Player import Player  # 같은 디렉터리 상대 import


class PlayerLeft(Player):
    def __init__(self):
        super().__init__()  # 부모 __init__ 호출 추가

    def initialize(self):
        self.dir = 1
        self.character = Priest()  # Priest 인스턴스 생성
        self.character.initialize()

    def update(self, deltaTime, input_dir=None):  # 입력 매개변수 추가
        super().update(deltaTime, input_dir)  # 부모 update 호출

    def render(self):
        self.character.render()

# from character.Priest import Priest  # SpriteManager 사용으로 주석 처리
from .Player import Player  # 같은 디렉터리 상대 import


class PlayerLeft(Player):
    def __init__(self):
        super().__init__()  # 부모 __init__ 호출 추가

    def initialize(self):
        self.dir = -1  # 오른쪽을 바라보도록 -1로 설정
        # self.character = Priest()  # SpriteManager 사용으로 주석 처리
        # self.character.initialize()  # SpriteManager 사용으로 주석 처리

    def update(self, deltaTime, input_dir=None):  # 입력 매개변수 추가
        super().update(deltaTime, input_dir)  # 부모 update 호출

    def render(self):
        # self.character.render()  # SpriteManager에서 렌더링하므로 주석 처리
        pass

# from character.Character import Character  # SpriteManager 사용으로 주석 처리


class Player:

    def __init__(self):

        self.x, self.y = 400, 300

        self.dir = -1  # 항상 오른쪽을 바라보도록 -1로 고정
        self.state = 'Idle'  # Idle, Walk
        # self.character = Character()  # SpriteManager 사용으로 주석 처리

    def initialize(self):
        # self.character.initialize()  # SpriteManager 사용으로 주석 처리
        pass

    def update(self, deltaTime, input_dir=None):  # 입력 방향 매개변수 추가
        if input_dir == 'left':
            self.x -= 5
            self.state = 'Walk'
            # self.dir = 1  # 방향 변경 제거
        elif input_dir == 'right':
            self.x += 5
            self.state = 'Walk'
            # self.dir = -1  # 방향 변경 제거
        else:
            self.state = 'Idle'  # 입력이 없으면 Idle 상태

        # self.character.update(deltaTime)  # SpriteManager 사용으로 주석 처리
        # self.character.x, self.character.y = self.x, self.y  # SpriteManager 사용으로 주석 처리

    def render(self):
        # self.character.render()  # SpriteManager에서 렌더링하므로 주석 처리
        pass

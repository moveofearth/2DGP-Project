# from character.Character import Character  # SpriteManager 사용으로 주석 처리


class Player:

    def __init__(self, x=400, y=300):  # 초기 위치를 매개변수로 받도록 수정
        self.x, self.y = x, y

        self.dir = -1  # 항상 오른쪽을 바라보도록 -1로 고정
        self.state = 'Idle'  # Idle, Walk, BackWalk
        # self.character = Character()  # SpriteManager 사용으로 주석 처리

    def initialize(self):
        # self.character.initialize()  # SpriteManager 사용으로 주석 처리
        pass

    def update(self, deltaTime, input_dir=None):  # 입력 방향 매개변수 추가
        if input_dir == 'left':
            self.x -= 5
            self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
        elif input_dir == 'right':
            self.x += 5
            self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
        else:
            self.state = 'Idle'  # 입력이 없으면 Idle 상태

        # self.character.update(deltaTime)  # SpriteManager 사용으로 주석 처리
        # self.character.x, self.character.y = self.x, self.y  # SpriteManager 사용으로 주석 처리

    def render(self):
        # self.character.render()  # SpriteManager에서 렌더링하므로 주석 처리
        pass

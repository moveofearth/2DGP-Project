from character.Character import Character  # import 수정: 패키지.모듈 import 클래스


class Player:

    def __init__(self):

        self.x, self.y = 400, 300

        self.dir = 0  # right -1, left 1
        self.state = 'Idle'  # Idle, Walk
        self.character = Character()  # _Character 오타 수정, 클래스 인스턴스 생성

    def initialize(self):
        self.character.initialize()  # 캐릭터 초기화 호출 추가

    def update(self, deltaTime, input_dir=None):  # 입력 방향 매개변수 추가

        if input_dir == 'left':
            self.x -= 5

            self.state = 'Walk'
            self.dir = 1
        elif input_dir == 'right':
            self.x += 5
            self.state = 'Walk'
            self.dir = -1
        self.character.update(deltaTime)  # 캐릭터 업데이트 연결
        self.character.x, self.character.y = self.x, self.y  # 위치 동기화

    def render(self):
        self.character.render()  # 캐릭터 렌더링 연결

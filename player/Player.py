# from character.Character import Character  # SpriteManager 사용으로 주석 처리


class Player:

    def __init__(self, x=400, y=300):  # 초기 위치를 매개변수로 받도록 수정
        self.x, self.y = x, y

        self.dir = -1  # 항상 오른쪽을 바라보도록 -1로 고정
        self.state = 'Idle'  # Idle, Walk, BackWalk
        self.is_attacking = False  # 공격 중인지 체크


    def is_attack_state(self):
        """현재 상태가 공격 상태인지 확인"""
        attack_states = ['fastMiddleATK', 'strongMiddleATK']  # strongMiddleATK 추가
        return self.state in attack_states

    def initialize(self):
        # self.character.initialize()  # SpriteManager 사용으로 주석 처리
        pass

    def update(self, deltaTime, move_input=None, atk_input=None):  # 이동과 공격 입력을 분리
        # 공격 입력 처리 (이동 중에도 가능)
        if atk_input == 'fastMiddleATK' and not self.is_attacking:
            self.state = 'fastMiddleATK'
            self.is_attacking = True
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongMiddleATK' and not self.is_attacking:
            self.state = 'strongMiddleATK'
            self.is_attacking = True
            return  # 공격 시작 시 이동은 무시

        # 공격 중이 아닐 때만 이동 처리
        if not self.is_attacking:
            if move_input == 'left':
                self.x -= 5
                self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
            elif move_input == 'right':
                self.x += 5
                self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
            else:
                self.state = 'Idle'  # 입력이 없으면 Idle 상태



    def render(self):
        pass

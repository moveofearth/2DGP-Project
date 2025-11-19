from .player import Player
import pico2d
import config


class PlayerRight(Player):
    def __init__(self):
        super().__init__(x=800, y=config.GROUND_Y, character_type='priest')  # priest 캐릭터로 초기화, x 위치를 더 오른쪽으로

    def initialize(self):
        super().initialize()
        self.dir = 1  # 왼쪽을 바라보도록 1로 설정
        self.hp = 100  # HP 초기화
        self.character.hp = self.hp  # Character HP 동기화
        self.y = config.GROUND_Y  # 그라운드에 위치
        self.is_grounded = True  # 지면에 있음

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False, char_change_input=None, other_player=None, position_state='Middle'):
        # 위치 상태 업데이트
        self.position_state = position_state

        # 부모 클래스의 업데이트 로직 호출 (position_state 포함)
        super().update(deltaTime, move_input, atk_input, combo_input, char_change_input, other_player, position_state)

        # PlayerRight 특화 이동 처리 (공격 중이나 가드 중이 아닐 때만) - 충돌 처리 포함
        if not self.is_attacking and not self.is_guarding and not self.is_hit:
            move_speed = self.get_move_speed()
            if move_input == 'left':
                new_x = self.x - move_speed * deltaTime
                self.update_position(new_x, other_player)
                self.state = 'Walk'  # 왼쪽으로 갈 때 Walk
            elif move_input == 'right':
                new_x = self.x + move_speed * 0.5 * deltaTime  # 오른쪽은 느리게
                self.update_position(new_x, other_player)
                self.state = 'BackWalk'  # 오른쪽으로 갈 때 BackWalk
            elif not move_input:
                self.state = 'Idle'  # 입력이 없으면 Idle 상태

    def render(self):
        # 바운딩 박스 그리기
        pico2d.draw_rectangle(*self.get_bb())
        # HP 텍스트 렌더링
        self._render_hp_text()

    def get_bb(self):
        """바운딩 박스 좌표 반환 - PlayerRight용 (오른쪽으로 50, 아래로 50 이동)"""
        # 1.5배 스케일링 적용
        bb_width = 40 * 1.5  # 60
        bb_height = 50 * 1.5  # 75
        adjusted_x = self.x + (30 * 1.5)
        adjusted_y = self.y - (50 * 1.5)
        return adjusted_x - bb_width, adjusted_y - bb_height, adjusted_x + bb_width, adjusted_y + bb_height

    def get_attack_range_bb(self):
        """공격 범위의 바운딩 박스 반환 (PlayerRight 기준 - 왼쪽 방향)"""
        my_bb = self.get_bb()

        # fast 공격 범위: 바운딩 박스 왼쪽 끝에서 -20
        if 'fast' in self.state:
            attack_range = 20
            range_x2 = my_bb[0]  # 바운딩 박스 왼쪽 끝
            range_x1 = range_x2 - attack_range
            range_y1 = my_bb[1]
            range_y2 = my_bb[3]
            return range_x1, range_y1, range_x2, range_y2

        # strong 공격 범위
        elif 'strong' in self.state:
            attack_range = 30
            range_x2 = my_bb[0]
            range_x1 = range_x2 - attack_range
            range_y1 = my_bb[1]
            range_y2 = my_bb[3]
            return range_x1, range_y1, range_x2, range_y2

        # rage 스킬 범위
        elif 'rage' in self.state:
            attack_range = 50
            range_x2 = my_bb[0]
            range_x1 = range_x2 - attack_range
            range_y1 = my_bb[1]
            range_y2 = my_bb[3]
            return range_x1, range_y1, range_x2, range_y2

        return None

import pico2d
import pathlib

class SpriteManager:
    def __init__(self):
        self.player1_sprite = None
        self.player2_sprite = None
        self.player1_state = 'Idle'
        self.player2_state = 'Idle'
        self.player1_frame = 0
        self.player2_frame = 0
        self.frame_time = 0.1  # 프레임 전환 시간
        self.frame_timer = 0.0  # 프레임 타이머
        self.player2_frame_timer = 0.0  # 플레이어2용 프레임 타이머
        self.player1_x = 400
        self.player1_y = 300
        self.player1_dir = -1  # 방향 (1: 왼쪽, -1: 오른쪽)
        self.player2_x = 600  # 플레이어2 초기 위치
        self.player2_y = 300
        self.player2_dir = -1
        self.player1_ref = None  # Player1 참조
        self.player2_ref = None  # Player2 참조

    def set_player_references(self, player1, player2):
        """플레이어 참조를 설정"""
        self.player1_ref = player1
        self.player2_ref = player2

    def load_sprites(self):
        base_path = pathlib.Path.cwd() / 'resources' / 'character'

        self.player1_sprite = {
            # temp image load
            'Idle': [pico2d.load_image(str(base_path / 'priest' / 'idle' / f'{i}.png')) for i in range(4)],
            'Walk': [pico2d.load_image(str(base_path / 'priest' / 'walk' / f'{i}.png')) for i in range(8)],
            'BackWalk': [pico2d.load_image(str(base_path / 'priest' / 'BackWalk' / f'{i}.png')) for i in range(8)], # BackWalk 추가
            'fastMiddleATK' : [pico2d.load_image(str(base_path / 'priest' / 'fastMiddleATK' / f'{i}.png')) for i in range(6)],
            'strongMiddleATK' : [pico2d.load_image(str(base_path / 'priest' / 'strongMiddleATK' / f'{i}.png')) for i in range(6)]
        }

        # 플레이어2도 같은 스프라이트 사용 (추후 다른 캐릭터로 변경 가능)
        self.player2_sprite = {
            'Idle': [pico2d.load_image(str(base_path / 'priest' / 'idle' / f'{i}.png')) for i in range(4)],
            'Walk': [pico2d.load_image(str(base_path / 'priest' / 'walk' / f'{i}.png')) for i in range(8)],
            'BackWalk': [pico2d.load_image(str(base_path / 'priest' / 'BackWalk' / f'{i}.png')) for i in range(8)],  # BackWalk 추가
            'fastMiddleATK': [pico2d.load_image(str(base_path / 'priest' / 'fastMiddleATK' / f'{i}.png')) for i in range(6)],
            'strongMiddleATK': [pico2d.load_image(str(base_path / 'priest' / 'strongMiddleATK' / f'{i}.png')) for i in range(6)]
        }

    def update_player1_state(self, new_state, deltaTime):
        # 상태가 변경되면 프레임을 0으로 리셋
        if self.player1_state != new_state:
            self.player1_state = new_state
            self.player1_frame = 0
            self.frame_timer = 0.0

        # 프레임 애니메이션 업데이트
        self.frame_timer += deltaTime
        if self.frame_timer >= self.frame_time:
            self.frame_timer = 0.0
            if self.player1_sprite and self.player1_state in self.player1_sprite:
                sprite_count = len(self.player1_sprite[self.player1_state])

                # 다음 프레임으로 진행
                next_frame = (self.player1_frame + 1) % sprite_count

                # 공격 애니메이션이 한 번 완료되었는지 체크
                if (self.player1_ref and self.player1_ref.is_attack_state() and
                    next_frame == 0):  # 애니메이션이 한 바퀴 돌았을 때
                    self.player1_ref.is_attacking = False
                    self.player1_ref.state = 'Idle'
                    self.player1_state = 'Idle'
                    self.player1_frame = 0
                else:
                    self.player1_frame = next_frame

    def update_player1_position(self, x, y):
        self.player1_x = x
        self.player1_y = y

    def update_player1_direction(self, direction):
        self.player1_dir = direction

    # 플레이어2용 메서드 추가
    def update_player2_state(self, new_state, deltaTime):
        # 상태가 변경되면 프레임을 0으로 리셋
        if self.player2_state != new_state:
            self.player2_state = new_state
            self.player2_frame = 0
            self.player2_frame_timer = 0.0

        # 프레임 애니메이션 업데이트
        self.player2_frame_timer += deltaTime
        if self.player2_frame_timer >= self.frame_time:
            self.player2_frame_timer = 0.0
            if self.player2_sprite and self.player2_state in self.player2_sprite:
                sprite_count = len(self.player2_sprite[self.player2_state])

                # 다음 프레임으로 진행
                next_frame = (self.player2_frame + 1) % sprite_count

                # 공격 애니메이션이 한 번 완료되었는지 체크
                if (self.player2_ref and self.player2_ref.is_attack_state() and
                    next_frame == 0):  # 애니메이션이 한 바퀴 돌았을 때
                    self.player2_ref.is_attacking = False
                    self.player2_ref.state = 'Idle'
                    self.player2_state = 'Idle'
                    self.player2_frame = 0
                else:
                    self.player2_frame = next_frame

    def update_player2_position(self, x, y):
        self.player2_x = x
        self.player2_y = y

    def update_player2_direction(self, direction):
        self.player2_dir = direction

    def render(self):
        # 플레이어1 렌더링 (오른쪽을 바라봄)
        if self.player1_sprite and self.player1_state in self.player1_sprite:
            sprite_list = self.player1_sprite[self.player1_state]
            if sprite_list:
                frame = self.player1_frame % len(sprite_list)
                sprite_list[frame].draw(self.player1_x, self.player1_y)

        # 플레이어2 렌더링 (왼쪽을 바라봄)
        if self.player2_sprite and self.player2_state in self.player2_sprite:
            sprite_list = self.player2_sprite[self.player2_state]
            if sprite_list:
                frame = self.player2_frame % len(sprite_list)
                # 왼쪽을 바라보도록 좌우 반전
                sprite_list[frame].composite_draw(0, 'h', self.player2_x, self.player2_y)

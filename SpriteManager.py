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
        self.player1_x = 400
        self.player1_y = 300
        self.player1_dir = -1  # 방향 (1: 왼쪽, -1: 오른쪽)

    def load_sprites(self):
        base_path = pathlib.Path.cwd() / 'resources' / 'character'

        self.player1_sprite = {
            # temp image load
            'Idle': [pico2d.load_image(str(base_path / 'priest' / 'idle' / f'{i}.png')) for i in range(3)],
            'Walk': [pico2d.load_image(str(base_path / 'priest' / 'walk' / f'{i}.png')) for i in range(8)]
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
                self.player1_frame = (self.player1_frame + 1) % sprite_count

    def update_player1_position(self, x, y):
        self.player1_x = x
        self.player1_y = y

    def update_player1_direction(self, direction):
        self.player1_dir = direction

    def render(self):
        if self.player1_sprite and self.player1_state in self.player1_sprite:
            sprite_list = self.player1_sprite[self.player1_state]
            if sprite_list:
                frame = self.player1_frame % len(sprite_list)
                # 항상 오른쪽을 바라보도록 좌우 반전 없이 그대로 그리기
                sprite_list[frame].draw(self.player1_x, self.player1_y)

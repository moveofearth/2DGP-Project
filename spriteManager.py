import pico2d
import pathlib

class SpriteManager:
    def __init__(self):
        self.shared_sprites = {}  # 캐릭터별 공유 스프라이트 딕셔너리
        self.player1_state = 'Idle'
        self.player2_state = 'Idle'
        self.player1_frame = 0
        self.player2_frame = 0
        self.frame_time = 0.5  # 프레임 전환 시간을 0.5초로 설정
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
        base_path = pathlib.Path.cwd() / 'Resources' / 'Character'

        # Priest 캐릭터 스프라이트 로딩
        self.shared_sprites['priest'] = {
            'Idle': [pico2d.load_image(str(base_path / 'priest' / 'idle' / f'{i}.png')) for i in range(4)],
            'Walk': [pico2d.load_image(str(base_path / 'priest' / 'walk' / f'{i}.png')) for i in range(8)],
            'BackWalk': [pico2d.load_image(str(base_path / 'priest' / 'BackWalk' / f'{i}.png')) for i in range(8)],
            'fastMiddleATK': [pico2d.load_image(str(base_path / 'priest' / 'fastMiddleATK' / f'{i}.png')) for i in range(6)],
            'strongMiddleATK': [pico2d.load_image(str(base_path / 'priest' / 'strongMiddleATK' / f'{i}.png')) for i in range(6)],
            'strongMiddleATK2': [pico2d.load_image(str(base_path / 'priest' / 'strongMiddleATK' / f'{i}.png')) for i in range(6, 14)],
            'strongUpperATK': [pico2d.load_image(str(base_path / 'priest' / 'strongUpperATK' / f'{i}.png')) for i in range(13)],
            'strongLowerATK': [pico2d.load_image(str(base_path / 'priest' / 'strongLowerATK' / f'{i}.png')) for i in range(9)]
        }

        # thief 캐릭터 스프라이트 로딩 (경로명을 'thief'로 수정)
        self.shared_sprites['thief'] = {
            'Idle': [pico2d.load_image(str(base_path / 'thief' / 'idle' / f'{i}.png')) for i in range(5)],
            'Walk': [pico2d.load_image(str(base_path / 'thief' / 'walk' / f'{i}.png')) for i in range(6)],
            'BackWalk': [pico2d.load_image(str(base_path / 'thief' / 'BackWalk' / f'{i}.png')) for i in range(7)],
            'fastMiddleATK': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(6)],  # 첫 번째 동작 (0~5)
            'fastMiddleATK2': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(6, 12)],  # 두 번째 동작 (6~11)
            'fastMiddleATK3': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(12, 18)],  # 세 번째 동작 (12~17)
            'strongMiddleATK': [pico2d.load_image(str(base_path / 'thief' / 'strongMiddleATK' / f'{i}.png')) for i in range(5)],
            #'strongMiddleATK2': [pico2d.load_image(str(base_path / 'thief' / 'strongMiddleATK' / f'{i}.png')) for i in range(5, 10)],
            #'strongUpperATK': [pico2d.load_image(str(base_path / 'thief' / 'strongUpperATK' / f'{i}.png')) for i in range(13)],
            #'strongLowerATK': [pico2d.load_image(str(base_path / 'thief' / 'strongLowerATK' / f'{i}.png')) for i in range(9)]
        }

        # 추후 다른 캐릭터 추가 시
        # self.shared_sprites['warrior'] = { ... }

    def get_character_sprites(self, character_type):
        """캐릭터 타입에 따른 스프라이트 반환"""
        return self.shared_sprites.get(character_type, self.shared_sprites.get('priest', {}))

    def update_player1_state(self, new_state, deltaTime):
        # 상태가 변경되면 프레임을 0으로 리셋
        if self.player1_state != new_state:
            self.player1_state = new_state
            self.player1_frame = 0
            self.frame_timer = 0.0

        # 프레임 애니메이션 업데이트 (deltaTime 사용하되 0.5초마다 프레임 전환)
        self.frame_timer += deltaTime
        if self.frame_timer >= self.frame_time:
            self.frame_timer = 0.0

            # 플레이어1의 캐릭터 타입에 따른 스프라이트 가져오기
            character_type = self.player1_ref.get_character_type() if self.player1_ref else 'priest'
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player1_state in sprites:
                sprite_count = len(sprites[self.player1_state])

                # 다음 프레임으로 진행
                next_frame = (self.player1_frame + 1) % sprite_count

                # thief 캐릭터의 fastMiddleATK 연계 처리
                if (character_type == 'thief' and
                    self.player1_ref and
                    next_frame == 0):  # 애니메이션 완료

                    if self.player1_state == 'fastMiddleATK':
                        # 첫 번째 동작 완료 -> 두 번째 동작으로 전환
                        self.player1_ref.state = 'fastMiddleATK2'
                        return
                    elif self.player1_state == 'fastMiddleATK2':
                        # 두 번째 동작 완료 -> 세 번째 동작으로 전환
                        self.player1_ref.state = 'fastMiddleATK3'
                        return
                    elif self.player1_state == 'fastMiddleATK3':
                        # 세 번째 동작 완료 -> 공격 종료
                        self.player1_ref.is_attacking = False
                        self.player1_ref.state = 'Idle'
                        self.player1_state = 'Idle'
                        self.player1_frame = 0
                        return

                # strongMiddleATK 완료 시 연계 공격 체크
                elif (self.player1_state == 'strongMiddleATK' and
                    self.player1_ref and
                    next_frame == 0):  # strongMiddleATK 애니메이션 완료

                    if self.player1_ref.combo_reserved:  # 연계가 예약되어 있으면
                        self.player1_ref.state = 'strongMiddleATK2'
                        self.player1_ref.combo_reserved = False
                        self.player1_ref.can_combo = False
                        return  # strongMiddleATK2로 상태 변경을 위해 리턴
                    else:  # 연계가 없으면 공격 종료
                        self.player1_ref.is_attacking = False
                        self.player1_ref.state = 'Idle'
                        self.player1_state = 'Idle'
                        self.player1_frame = 0
                        self.player1_ref.can_combo = False
                        return

                # 다른 공격 애니메이션 완료 처리
                elif (self.player1_ref and self.player1_ref.is_attack_state() and
                      self.player1_state not in ['strongMiddleATK', 'fastMiddleATK', 'fastMiddleATK2'] and
                      next_frame == 0):
                    self.player1_ref.is_attacking = False
                    self.player1_ref.state = 'Idle'
                    self.player1_state = 'Idle'
                    self.player1_frame = 0
                    self.player1_ref.can_combo = False
                else:
                    self.player1_frame = next_frame

        # strongMiddleATK에서 연계 가능 시점 체크
        if (self.player1_state == 'strongMiddleATK' and
            self.player1_ref and
            self.player1_frame >= 3):  # 3프레임 이후부터 연계 가능
            self.player1_ref.can_combo = True

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

        # 프레임 애니메이션 업데이트 (deltaTime 사용하되 0.5초마다 프레임 전환)
        self.player2_frame_timer += deltaTime
        if self.player2_frame_timer >= self.frame_time:
            self.player2_frame_timer = 0.0

            # 플레이어2의 캐릭터 타입에 따른 스프라이트 가져오기
            character_type = self.player2_ref.get_character_type() if self.player2_ref else 'priest'
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player2_state in sprites:
                sprite_count = len(sprites[self.player2_state])
                next_frame = (self.player2_frame + 1) % sprite_count

                # thief 캐릭터의 fastMiddleATK 연계 처리
                if (character_type == 'thief' and
                    self.player2_ref and
                    next_frame == 0):  # 애니메이션 완료

                    if self.player2_state == 'fastMiddleATK':
                        # 첫 번째 동작 완료 -> 두 번째 동작으로 전환
                        self.player2_ref.state = 'fastMiddleATK2'
                        return
                    elif self.player2_state == 'fastMiddleATK2':
                        # 두 번째 동작 완료 -> 세 번째 동작으로 전환
                        self.player2_ref.state = 'fastMiddleATK3'
                        return
                    elif self.player2_state == 'fastMiddleATK3':
                        # 세 번째 동작 완료 -> 공격 종료
                        self.player2_ref.is_attacking = False
                        self.player2_ref.state = 'Idle'
                        self.player2_state = 'Idle'
                        self.player2_frame = 0
                        return

                # strongMiddleATK 완료 시 연계 공격 체크
                elif (self.player2_state == 'strongMiddleATK' and
                    self.player2_ref and
                    next_frame == 0):  # strongMiddleATK 애니메이션 완료

                    if self.player2_ref.combo_reserved:  # 연계가 예약되어 있으면
                        self.player2_ref.state = 'strongMiddleATK2'
                        self.player2_ref.combo_reserved = False
                        self.player2_ref.can_combo = False
                        return  # strongMiddleATK2로 상태 변경을 위해 리턴
                    else:  # 연계가 없으면 공격 종료
                        self.player2_ref.is_attacking = False
                        self.player2_ref.state = 'Idle'
                        self.player2_state = 'Idle'
                        self.player2_frame = 0
                        self.player2_ref.can_combo = False
                        return

                # 다른 공격 애니메이션 완료 처리
                elif (self.player2_ref and self.player2_ref.is_attack_state() and
                      self.player2_state not in ['strongMiddleATK', 'fastMiddleATK', 'fastMiddleATK2'] and
                      next_frame == 0):
                    self.player2_ref.is_attacking = False
                    self.player2_ref.state = 'Idle'
                    self.player2_state = 'Idle'
                    self.player2_frame = 0
                    self.player2_ref.can_combo = False
                else:
                    self.player2_frame = next_frame

        # strongMiddleATK에서 연계 가능 시점 체크
        if (self.player2_state == 'strongMiddleATK' and
            self.player2_ref and
            self.player2_frame >= 3):  # 3프레임 이후부터 연계 가능
            self.player2_ref.can_combo = True

    def update_player2_position(self, x, y):
        self.player2_x = x
        self.player2_y = y

    def update_player2_direction(self, direction):
        self.player2_dir = direction

    def render(self):
        # 플레이어1 렌더링 (오른쪽을 바라봄)
        if self.player1_ref:
            character_type = self.player1_ref.get_character_type()
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player1_state in sprites:
                sprite_list = sprites[self.player1_state]
                if sprite_list:
                    frame = self.player1_frame % len(sprite_list)
                    sprite_list[frame].draw(self.player1_x, self.player1_y)

        # 플레이어2 렌더링 (왼쪽을 바라봄)
        if self.player2_ref:
            character_type = self.player2_ref.get_character_type()
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player2_state in sprites:
                sprite_list = sprites[self.player2_state]
                if sprite_list:
                    frame = self.player2_frame % len(sprite_list)
                    # 왼쪽을 바라보도록 좌우 반전
                    sprite_list[frame].composite_draw(0, 'h', self.player2_x, self.player2_y)

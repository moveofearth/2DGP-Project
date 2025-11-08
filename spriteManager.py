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

        # thief 캐릭터 스프라이트 로딩
        self.shared_sprites['thief'] = {
            'Idle': [pico2d.load_image(str(base_path / 'thief' / 'idle' / f'{i}.png')) for i in range(6)],  # 0~5로 수정 (6개)
            'Walk': [pico2d.load_image(str(base_path / 'thief' / 'walk' / f'{i}.png')) for i in range(6)],
            'BackWalk': [pico2d.load_image(str(base_path / 'thief' / 'BackWalk' / f'{i}.png')) for i in range(7)],
            'fastMiddleATK': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(6)],
            'fastMiddleATK2': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(6, 12)],
            'fastMiddleATK3': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(12, 18)],
            'strongMiddleATK': [pico2d.load_image(str(base_path / 'thief' / 'strongMiddleATK' / f'{i}.png')) for i in range(5)],  # 0~4
            'strongMiddleATK2': [pico2d.load_image(str(base_path / 'thief' / 'strongMiddleATK' / f'{i}.png')) for i in range(5, 10)],  # 5~9
            'strongUpperATK': [pico2d.load_image(str(base_path / 'thief' / 'strongUpperATK' / f'{i}.png')) for i in range(5)],  # 0~4
            'strongUpperATK2': [pico2d.load_image(str(base_path / 'thief' / 'strongUpperATK' / f'{i}.png')) for i in range(5, 10)],  # 5~9
            'strongLowerATK': [pico2d.load_image(str(base_path / 'thief' / 'strongLowerATK' / f'{i}.png')) for i in range(4)]  # 0~3
        }

    def get_character_sprites(self, character_type):
        """캐릭터 타입에 따른 스프라이트 반환"""
        return self.shared_sprites.get(character_type, self.shared_sprites.get('priest', {}))

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

            # 플레이어1의 캐릭터 타입에 따른 스프라이트 가져오기
            character_type = self.player1_ref.get_character_type() if self.player1_ref else 'priest'
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player1_state in sprites:
                sprite_count = len(sprites[self.player1_state])
                next_frame = (self.player1_frame + 1) % sprite_count

                # 공격 상태가 아닌 경우 (Idle, Walk, BackWalk) 단순히 다음 프레임으로 진행
                if self.player1_state in ['Idle', 'Walk', 'BackWalk']:
                    self.player1_frame = next_frame
                    return

                # thief 캐릭터의 연계 처리
                if (character_type == 'thief' and
                    self.player1_ref and
                    next_frame == 0):  # 애니메이션 완료

                    if self.player1_state == 'fastMiddleATK':
                        # 첫 번째 동작 완료 - F키 입력 대기
                        if self.player1_ref.combo_reserved:
                            self.player1_ref.state = 'fastMiddleATK2'
                            self.player1_ref.combo_reserved = False
                            self.player1_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player1_ref.is_attacking = False
                            self.player1_ref.state = 'Idle'
                            self.player1_state = 'Idle'
                            self.player1_frame = 0
                            self.player1_ref.can_combo = False
                            return
                    elif self.player1_state == 'fastMiddleATK2':
                        # 두 번째 동작 완료 - F키 입력 대기
                        if self.player1_ref.combo_reserved:
                            self.player1_ref.state = 'fastMiddleATK3'
                            self.player1_ref.combo_reserved = False
                            self.player1_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player1_ref.is_attacking = False
                            self.player1_ref.state = 'Idle'
                            self.player1_state = 'Idle'
                            self.player1_frame = 0
                            self.player1_ref.can_combo = False
                            return
                    elif self.player1_state == 'fastMiddleATK3':
                        # 세 번째 동작 완료 -> 공격 종료
                        self.player1_ref.is_attacking = False
                        self.player1_ref.state = 'Idle'
                        self.player1_state = 'Idle'
                        self.player1_frame = 0
                        return
                    elif self.player1_state == 'strongMiddleATK':
                        # thief의 strongMiddleATK도 G키 입력 대기
                        if self.player1_ref.combo_reserved:
                            self.player1_ref.state = 'strongMiddleATK2'
                            self.player1_ref.combo_reserved = False
                            self.player1_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player1_ref.is_attacking = False
                            self.player1_ref.state = 'Idle'
                            self.player1_state = 'Idle'
                            self.player1_frame = 0
                            self.player1_ref.can_combo = False
                            return
                    elif self.player1_state == 'strongMiddleATK2':
                        # strongMiddleATK2 완료 -> 공격 종료
                        self.player1_ref.is_attacking = False
                        self.player1_ref.state = 'Idle'
                        self.player1_state = 'Idle'
                        self.player1_frame = 0
                        return
                    elif self.player1_state == 'strongUpperATK':
                        # thief의 strongUpperATK도 G키 입력 대기
                        if self.player1_ref.combo_reserved:
                            self.player1_ref.state = 'strongUpperATK2'
                            self.player1_ref.combo_reserved = False
                            self.player1_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player1_ref.is_attacking = False
                            self.player1_ref.state = 'Idle'
                            self.player1_state = 'Idle'
                            self.player1_frame = 0
                            self.player1_ref.can_combo = False
                            return
                    elif self.player1_state == 'strongUpperATK2':
                        # strongUpperATK2 완료 -> 공격 종료
                        self.player1_ref.is_attacking = False
                        self.player1_ref.state = 'Idle'
                        self.player1_state = 'Idle'
                        self.player1_frame = 0
                        return
                    elif self.player1_state == 'strongLowerATK':
                        # thief의 strongLowerATK 완료 -> 공격 종료 (연계 없음)
                        self.player1_ref.is_attacking = False
                        self.player1_ref.state = 'Idle'
                        self.player1_state = 'Idle'
                        self.player1_frame = 0
                        return

                # priest 캐릭터의 strongMiddleATK 연계 처리
                elif (character_type == 'priest' and
                      self.player1_state == 'strongMiddleATK' and
                      self.player1_ref and
                      next_frame == 0):

                    if self.player1_ref.combo_reserved:
                        self.player1_ref.state = 'strongMiddleATK2'
                        self.player1_ref.combo_reserved = False
                        self.player1_ref.can_combo = False
                        return
                    else:
                        self.player1_ref.is_attacking = False
                        self.player1_ref.state = 'Idle'
                        self.player1_state = 'Idle'
                        self.player1_frame = 0
                        self.player1_ref.can_combo = False
                        return

                # 다른 공격 애니메이션 완료 처리
                elif (self.player1_ref and self.player1_ref.is_attack_state() and
                      next_frame == 0):
                    self.player1_ref.is_attacking = False
                    self.player1_ref.state = 'Idle'
                    self.player1_state = 'Idle'
                    self.player1_frame = 0
                    if hasattr(self.player1_ref, 'can_combo'):
                        self.player1_ref.can_combo = False
                else:
                    self.player1_frame = next_frame

        # 연계 가능 시점 체크
        character_type = self.player1_ref.get_character_type() if self.player1_ref else 'priest'
        if (character_type == 'priest' and
            self.player1_state == 'strongMiddleATK' and
            self.player1_ref and
            self.player1_frame >= 3):
            self.player1_ref.can_combo = True
        # thief의 연계 가능 시점 체크
        elif (character_type == 'thief' and
              (self.player1_state in ['fastMiddleATK', 'fastMiddleATK2', 'strongMiddleATK', 'strongUpperATK']) and
              self.player1_ref and
              self.player1_frame >= 3):  # 3프레임 이후부터 연계 가능
            self.player1_ref.can_combo = True

    def update_player1_position(self, x, y):
        self.player1_x = x
        self.player1_y = y

    def update_player1_direction(self, direction):
        self.player1_dir = direction

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

            # 플레이어2의 캐릭터 타입에 따른 스프라이트 가져오기
            character_type = self.player2_ref.get_character_type() if self.player2_ref else 'priest'
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player2_state in sprites:
                sprite_count = len(sprites[self.player2_state])
                next_frame = (self.player2_frame + 1) % sprite_count

                # 공격 상태가 아닌 경우 (Idle, Walk, BackWalk) 단순히 다음 프레임으로 진행
                if self.player2_state in ['Idle', 'Walk', 'BackWalk']:
                    self.player2_frame = next_frame
                    return

                # thief 캐릭터의 연계 처리
                if (character_type == 'thief' and
                    self.player2_ref and
                    next_frame == 0):

                    if self.player2_state == 'fastMiddleATK':
                        # 첫 번째 동작 완료 - 1키 입력 대기
                        if self.player2_ref.combo_reserved:
                            self.player2_ref.state = 'fastMiddleATK2'
                            self.player2_ref.combo_reserved = False
                            self.player2_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player2_ref.is_attacking = False
                            self.player2_ref.state = 'Idle'
                            self.player2_state = 'Idle'
                            self.player2_frame = 0
                            self.player2_ref.can_combo = False
                            return
                    elif self.player2_state == 'fastMiddleATK2':
                        # 두 번째 동작 완료 - 1키 입력 대기
                        if self.player2_ref.combo_reserved:
                            self.player2_ref.state = 'fastMiddleATK3'
                            self.player2_ref.combo_reserved = False
                            self.player2_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player2_ref.is_attacking = False
                            self.player2_ref.state = 'Idle'
                            self.player2_state = 'Idle'
                            self.player2_frame = 0
                            self.player2_ref.can_combo = False
                            return
                    elif self.player2_state == 'fastMiddleATK3':
                        # 세 번째 동작 완료 -> 공격 종료
                        self.player2_ref.is_attacking = False
                        self.player2_ref.state = 'Idle'
                        self.player2_state = 'Idle'
                        self.player2_frame = 0
                        return
                    elif self.player2_state == 'strongMiddleATK':
                        # thief의 strongMiddleATK도 2키 입력 대기
                        if self.player2_ref.combo_reserved:
                            self.player2_ref.state = 'strongMiddleATK2'
                            self.player2_ref.combo_reserved = False
                            self.player2_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player2_ref.is_attacking = False
                            self.player2_ref.state = 'Idle'
                            self.player2_state = 'Idle'
                            self.player2_frame = 0
                            self.player2_ref.can_combo = False
                            return
                    elif self.player2_state == 'strongMiddleATK2':
                        # strongMiddleATK2 완료 -> 공격 종료
                        self.player2_ref.is_attacking = False
                        self.player2_ref.state = 'Idle'
                        self.player2_state = 'Idle'
                        self.player2_frame = 0
                        return
                    elif self.player2_state == 'strongUpperATK':
                        # thief의 strongUpperATK도 2키 입력 대기
                        if self.player2_ref.combo_reserved:
                            self.player2_ref.state = 'strongUpperATK2'
                            self.player2_ref.combo_reserved = False
                            self.player2_ref.can_combo = False
                            return
                        else:
                            # 연계 입력이 없으면 공격 종료
                            self.player2_ref.is_attacking = False
                            self.player2_ref.state = 'Idle'
                            self.player2_state = 'Idle'
                            self.player2_frame = 0
                            self.player2_ref.can_combo = False
                            return
                    elif self.player2_state == 'strongUpperATK2':
                        # strongUpperATK2 완료 -> 공격 종료
                        self.player2_ref.is_attacking = False
                        self.player2_ref.state = 'Idle'
                        self.player2_state = 'Idle'
                        self.player2_frame = 0
                        return
                    elif self.player2_state == 'strongLowerATK':
                        # thief의 strongLowerATK 완료 -> 공격 종료 (연계 없음)
                        self.player2_ref.is_attacking = False
                        self.player2_ref.state = 'Idle'
                        self.player2_state = 'Idle'
                        self.player2_frame = 0
                        return

                # priest 캐릭터의 strongMiddleATK 연계 처리
                elif (character_type == 'priest' and
                      self.player2_state == 'strongMiddleATK' and
                      self.player2_ref and
                      next_frame == 0):

                    if self.player2_ref.combo_reserved:
                        self.player2_ref.state = 'strongMiddleATK2'
                        self.player2_ref.combo_reserved = False
                        self.player2_ref.can_combo = False
                        return
                    else:
                        self.player2_ref.is_attacking = False
                        self.player2_ref.state = 'Idle'
                        self.player2_state = 'Idle'
                        self.player2_frame = 0
                        self.player2_ref.can_combo = False
                        return

                # 다른 공격 애니메이션 완료 처리
                elif (self.player2_ref and self.player2_ref.is_attack_state() and
                      next_frame == 0):
                    self.player2_ref.is_attacking = False
                    self.player2_ref.state = 'Idle'
                    self.player2_state = 'Idle'
                    self.player2_frame = 0
                else:
                    self.player2_frame = next_frame

        # 연계 가능 시점 체크
        character_type = self.player2_ref.get_character_type() if self.player2_ref else 'priest'
        if (character_type == 'priest' and
            self.player2_state == 'strongMiddleATK' and
            self.player2_ref and
            self.player2_frame >= 3):
            self.player2_ref.can_combo = True
        # thief의 연계 가능 시점 체크
        elif (character_type == 'thief' and
              (self.player2_state in ['fastMiddleATK', 'fastMiddleATK2', 'strongMiddleATK', 'strongUpperATK']) and
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

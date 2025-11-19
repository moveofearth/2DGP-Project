import pico2d
import pathlib
import config

class SpriteManager:
    def __init__(self):
        self.shared_sprites = {}  # 캐릭터별 공유 스프라이트 딕셔너리
        self.player1_state = 'Idle'
        self.player2_state = 'Idle'
        self.player1_frame = 0
        self.player2_frame = 0
        self.default_frame_time = 0.083  # 기본 프레임 전환 시간 (약 12fps)
        self.fast_attack_frame_time = 0.1  # fast 공격 프레임 시간
        self.strong_attack_frame_time = 0.15  # strong 공격 프레임 시간
        self.frame_timer = 0.0  # 프레임 타이머
        self.player2_frame_timer = 0.0  # 플레이어2용 프레임 타이머
        # 1280x720 -> 1920x1080 스케일링을 위한 배율
        self.scale_factor = 1.5

        # 플레이어 초기 위치도 스케일링 - 그라운드에 위치, 충돌하지 않도록 간격 조정
        self.player1_x = 400 * self.scale_factor  # 600
        self.player1_y = config.GROUND_Y  # 그라운드에 위치
        self.player1_dir = -1  # 방향 (1: 왼쪽, -1: 오른쪽)
        self.player2_x = 600 * self.scale_factor  # 900 (더 넓은 간격)
        self.player2_y = config.GROUND_Y  # 그라운드에 위치
        self.player2_dir = -1
        self.player1_ref = None  # Player1 참조
        self.player2_ref = None  # Player2 참조
        self.rage_skill_frame_time = 1.0 / 18  # 1초 동안 18프레임 (0~17)

        # 캐릭터 타입 추적
        self.player1_character_type = 'thief'
        self.player2_character_type = 'priest'

        # 캐릭터별 y 위치 오프셋도 스케일링
        self.character_y_offsets = {
            'priest': 0,
            'thief': -20 * self.scale_factor,    # -30
            'fighter': -30 * self.scale_factor   # -45
        }

    def set_player_references(self, player1, player2):
        """플레이어 참조를 설정"""
        self.player1_ref = player1
        self.player2_ref = player2
        # 초기 캐릭터 타입 설정
        if player1:
            self.player1_character_type = player1.get_character_type()
        if player2:
            self.player2_character_type = player2.get_character_type()

    def load_sprites(self):
        """스프라이트 로딩 - 예외 처리 추가"""
        try:
            base_path = pathlib.Path.cwd() / 'Resources' / 'Character'

            # Priest 캐릭터 스프라이트 로딩
            self.shared_sprites['priest'] = {
                'Idle': [pico2d.load_image(str(base_path / 'priest' / 'idle' / f'{i}.png')) for i in range(4)],
                'Walk': [pico2d.load_image(str(base_path / 'priest' / 'walk' / f'{i}.png')) for i in range(8)],
                'BackWalk': [pico2d.load_image(str(base_path / 'priest' / 'BackWalk' / f'{i}.png')) for i in range(8)],
                'fastMiddleATK': [pico2d.load_image(str(base_path / 'priest' / 'fastMiddleATK' / f'{i}.png')) for i in range(6)],
                'strongMiddleATK': [pico2d.load_image(str(base_path / 'priest' / 'strongMiddleATK' / f'{i}.png')) for i in range(6)],
                'strongMiddleATK2': [pico2d.load_image(str(base_path / 'priest' / 'strongMiddleATK' / f'{i}.png')) for i in range(6, 14)],
                'strongUpperATK': [pico2d.load_image(str(base_path / 'priest' / 'strongUpperATK' / f'{i}.png')) for i in range(12)],
                'strongLowerATK': [pico2d.load_image(str(base_path / 'priest' / 'strongLowerATK' / f'{i}.png')) for i in range(9)],
                'rageSkill': [pico2d.load_image(str(base_path / 'priest' / 'rageSkill' / f'{i}.png')) for i in range(18)],
                'hit': [pico2d.load_image(str(base_path / 'priest' / 'hit' / f'{i}.png')) for i in range(6)],
                'guard': [pico2d.load_image(str(base_path / 'priest' / 'guard' / f'{i}.png')) for i in range(2)]  # Guard 스프라이트 추가 (0~1)
            }

            # thief 캐릭터 스프라이트 로딩
            self.shared_sprites['thief'] = {
                'Idle': [pico2d.load_image(str(base_path / 'thief' / 'idle' / f'{i}.png')) for i in range(6)],
                'Walk': [pico2d.load_image(str(base_path / 'thief' / 'walk' / f'{i}.png')) for i in range(6)],
                'BackWalk': [pico2d.load_image(str(base_path / 'thief' / 'BackWalk' / f'{i}.png')) for i in range(7)],
                'fastMiddleATK': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(6)],
                'fastMiddleATK2': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(6, 12)],
                'fastMiddleATK3': [pico2d.load_image(str(base_path / 'thief' / 'fastMiddleATK' / f'{i}.png')) for i in range(12, 18)],
                'strongMiddleATK': [pico2d.load_image(str(base_path / 'thief' / 'strongMiddleATK' / f'{i}.png')) for i in range(5)],
                'strongMiddleATK2': [pico2d.load_image(str(base_path / 'thief' / 'strongMiddleATK' / f'{i}.png')) for i in range(5, 10)],
                'strongUpperATK': [pico2d.load_image(str(base_path / 'thief' / 'strongUpperATK' / f'{i}.png')) for i in range(5)],
                'strongUpperATK2': [pico2d.load_image(str(base_path / 'thief' / 'strongUpperATK' / f'{i}.png')) for i in range(5, 10)],
                'strongLowerATK': [pico2d.load_image(str(base_path / 'thief' / 'strongLowerATK' / f'{i}.png')) for i in range(4)]
            }

            # fighter 캐릭터 스프라이트 로딩
            self.shared_sprites['fighter'] = {
                'Idle': [pico2d.load_image(str(base_path / 'fighter' / 'idle' / f'{i}.png')) for i in range(4)],
                'Walk': [pico2d.load_image(str(base_path / 'fighter' / 'walk' / f'{i}.png')) for i in range(8)],
                'BackWalk': [pico2d.load_image(str(base_path / 'fighter' / 'BackWalk' / f'{i}.png')) for i in range(5)],
                'fastMiddleATK': [pico2d.load_image(str(base_path / 'fighter' / 'fastMiddleATK' / f'{i}.png')) for i in range(4)],
                'fastMiddleATK2': [pico2d.load_image(str(base_path / 'fighter' / 'fastMiddleATK' / f'{i}.png')) for i in range(4, 7)],
                'fastMiddleATK3': [pico2d.load_image(str(base_path / 'fighter' / 'fastMiddleATK' / f'{i}.png')) for i in range(7, 10)],
                'strongMiddleATK': [pico2d.load_image(str(base_path / 'fighter' / 'strongMiddleATK' / f'{i}.png')) for i in range(5)],
                'strongLowerATK': [pico2d.load_image(str(base_path / 'fighter' / 'strongLowerATK' / f'{i}.png')) for i in range(5)],
                'strongUpperATK': [pico2d.load_image(str(base_path / 'fighter' / 'strongUpperATK' / f'{i}.png')) for i in range(4)],
                'strongUpperATK2': [pico2d.load_image(str(base_path / 'fighter' / 'strongUpperATK' / f'{i}.png')) for i in range(4, 8)],
                'fastLowerATK': [pico2d.load_image(str(base_path / 'fighter' / 'fastLowerATK' / f'{i}.png')) for i in range(4)],  # 0~3
                'fastUpperATK': [pico2d.load_image(str(base_path / 'fighter' / 'fastUpperATK' / f'{i}.png')) for i in range(6)]  # 0~5
            }
        except Exception as e:
            print(f"Warning: Sprite loading failed: {e}")
            # 기본 빈 딕셔너리로 초기화
            self.shared_sprites = {
                'priest': {}, 'thief': {}, 'fighter': {}
            }

    def get_character_sprites(self, character_type):
        """캐릭터 타입에 따른 스프라이트 반환"""
        return self.shared_sprites.get(character_type, self.shared_sprites.get('priest', {}))

    def _handle_animation_completion(self, player_ref, state, character_type, is_player1=True):
        """애니메이션 완료 시 처리 로직"""
        if not player_ref:
            return False

        # hit 상태 처리
        if state == 'hit':
            # hit 애니메이션이 완료되면 hit 상태 초기화
            player_ref.character.reset_hit_state()
            self._end_attack(player_ref, is_player1)
            return True

        # rage 스킬 완료 처리
        if state == 'rageSkill':
            self._end_attack(player_ref, is_player1)
            return True

        # 연계 공격 처리
        combo_mapping = {
            'priest': {
                'strongMiddleATK': 'strongMiddleATK2'
            },
            'thief': {
                'fastMiddleATK': 'fastMiddleATK2',
                'fastMiddleATK2': 'fastMiddleATK3',
                'strongMiddleATK': 'strongMiddleATK2',
                'strongUpperATK': 'strongUpperATK2'
            },
            'fighter': {
                'fastMiddleATK': 'fastMiddleATK2',
                'fastMiddleATK2': 'fastMiddleATK3',
                'strongUpperATK': 'strongUpperATK2'
            }
        }

        # 연계 가능한 상태인지 확인
        if (character_type in combo_mapping and
            state in combo_mapping[character_type]):

            if player_ref.combo_reserved:
                # 연계 실행
                next_state = combo_mapping[character_type][state]
                if is_player1:
                    self.player1_state = next_state
                    self.player1_frame = 0
                else:
                    self.player2_state = next_state
                    self.player2_frame = 0

                player_ref.state = next_state
                player_ref.combo_reserved = False
                player_ref.can_combo = False
                print(f"Combo executed: {state} -> {next_state}")
                return True
            else:
                # 연계 입력이 없으면 공격 종료
                self._end_attack(player_ref, is_player1)
                return True

        # 연계가 없는 공격이나 마지막 연계 완료 - 모든 공격 상태 포함
        self._end_attack(player_ref, is_player1)
        return True

    def _end_attack(self, player_ref, is_player1):
        """공격 종료 처리"""
        player_ref.is_attacking = False
        player_ref.state = 'Idle'
        player_ref.can_combo = False
        player_ref.combo_reserved = False

        if is_player1:
            self.player1_state = 'Idle'
            self.player1_frame = 0
        else:
            self.player2_state = 'Idle'
            self.player2_frame = 0

        print(f"Attack ended for player {'1' if is_player1 else '2'}")

    def _update_combo_availability(self, player_ref, state, character_type, frame):
        """연계 가능 시점 체크"""
        if not player_ref:
            return

        combo_frames = {
            'priest': {'strongMiddleATK': 3},
            'thief': {
                'fastMiddleATK': 3, 'fastMiddleATK2': 3,
                'strongMiddleATK': 3, 'strongUpperATK': 3
            },
            'fighter': {
                'fastMiddleATK': 2, 'fastMiddleATK2': 2,
                'strongUpperATK': 3
            }
        }

        if (character_type in combo_frames and
            state in combo_frames[character_type] and
            frame >= combo_frames[character_type][state]):
            if not player_ref.can_combo:
                player_ref.can_combo = True
                print(f"Combo available for {character_type} at frame {frame}")

    def _get_frame_time_for_state(self, state):
        """상태에 따른 프레임 시간 반환"""
        if state == 'hit':
            return 0.1  # hit 애니메이션 속도
        elif state == 'guard':
            return 0.025  # guard 애니메이션 속도 (빠르게)
        elif state == 'rageSkill':
            return self.rage_skill_frame_time
        elif 'fast' in state.lower():
            return self.fast_attack_frame_time
        elif 'strong' in state.lower():
            return self.strong_attack_frame_time
        else:
            return self.default_frame_time

    def update_player1_state(self, new_state, deltaTime):
        # 캐릭터 타입 변경 감지
        if self.player1_ref:
            current_character_type = self.player1_ref.get_character_type()
            if current_character_type != self.player1_character_type:
                self.player1_character_type = current_character_type
                self.player1_frame = 0
                self.frame_timer = 0.0
                print(f"Player1 character changed to: {current_character_type}")

        # 상태가 변경되면 프레임을 0으로 리셋
        if self.player1_state != new_state:
            print(f"Player1 state changed: {self.player1_state} -> {new_state}")
            self.player1_state = new_state
            self.player1_frame = 0
            self.frame_timer = 0.0
            # 새로운 공격 시작 시 타격 플래그 리셋
            if self.player1_ref and 'ATK' in new_state:
                self.player1_ref.reset_attack_hit_flag()

        # 현재 상태에 맞는 프레임 시간 가져오기
        current_frame_time = self._get_frame_time_for_state(self.player1_state)

        # 프레임 애니메이션 업데이트
        self.frame_timer += deltaTime
        if self.frame_timer >= current_frame_time:
            self.frame_timer = 0.0

            character_type = self.player1_character_type
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player1_state in sprites:
                sprite_count = len(sprites[self.player1_state])

                # 공격 애니메이션 절반 지점에서 타격 처리 활성화
                if self.player1_ref and 'ATK' in self.player1_state:
                    hit_frame = sprite_count // 2  # 애니메이션 절반 지점
                    if self.player1_frame == hit_frame:
                        self.player1_ref.can_process_hit = True

                # hit 상태 특별 처리
                if self.player1_state == 'hit' and self.player1_ref:
                    if self.player1_ref.character.hit_type == 'fast':
                        max_frame = 1
                    elif self.player1_ref.character.hit_type == 'strong':
                        max_frame = 4
                    else:
                        max_frame = sprite_count - 1

                    if self.player1_frame < max_frame:
                        self.player1_frame += 1
                    elif self.player1_frame == 4 and self.player1_ref.character.hit_type == 'strong':
                        if self.player1_ref.hit_recovery_input:
                            self.player1_frame = 5
                            self.player1_ref.hit_recovery_input = False
                    return

                next_frame = (self.player1_frame + 1) % sprite_count

                # 일반 상태는 단순 순환
                if self.player1_state in ['Idle', 'Walk', 'BackWalk', 'guard']:
                    self.player1_frame = next_frame
                    return

                # 공격 상태에서 애니메이션 완료 시 처리
                if next_frame == 0:  # 애니메이션 한 사이클 완료
                    if self._handle_animation_completion(
                        self.player1_ref, self.player1_state, character_type, True):
                        return

                self.player1_frame = next_frame

        # 연계 가능 시점 체크
        if self.player1_ref and self.player1_ref.is_attacking:
            self._update_combo_availability(
                self.player1_ref, self.player1_state, self.player1_character_type, self.player1_frame)

    def update_player2_state(self, new_state, deltaTime):
        # 캐릭터 타입 변경 감지
        if self.player2_ref:
            current_character_type = self.player2_ref.get_character_type()
            if current_character_type != self.player2_character_type:
                self.player2_character_type = current_character_type
                self.player2_frame = 0
                self.player2_frame_timer = 0.0
                print(f"Player2 character changed to: {current_character_type}")

        # 상태가 변경되면 프레임을 0으로 리셋
        if self.player2_state != new_state:
            print(f"Player2 state changed: {self.player2_state} -> {new_state}")
            self.player2_state = new_state
            self.player2_frame = 0
            self.player2_frame_timer = 0.0
            # 새로운 공격 시작 시 타격 플래그 리셋
            if self.player2_ref and 'ATK' in new_state:
                self.player2_ref.reset_attack_hit_flag()

        # 현재 상태에 맞는 프레임 시간 가져오기
        current_frame_time = self._get_frame_time_for_state(self.player2_state)

        # 프레임 애니메이션 업데이트
        self.player2_frame_timer += deltaTime
        if self.player2_frame_timer >= current_frame_time:
            self.player2_frame_timer = 0.0

            character_type = self.player2_character_type
            sprites = self.get_character_sprites(character_type)

            if sprites and self.player2_state in sprites:
                sprite_count = len(sprites[self.player2_state])

                # 공격 애니메이션 절반 지점에서 타격 처리 활성화
                if self.player2_ref and 'ATK' in self.player2_state:
                    hit_frame = sprite_count // 2  # 애니메이션 절반 지점
                    if self.player2_frame == hit_frame:
                        self.player2_ref.can_process_hit = True

                # hit 상태 특별 처리
                if self.player2_state == 'hit' and self.player2_ref:
                    if self.player2_ref.character.hit_type == 'fast':
                        max_frame = 1
                    elif self.player2_ref.character.hit_type == 'strong':
                        max_frame = 4
                    else:
                        max_frame = sprite_count - 1

                    if self.player2_frame < max_frame:
                        self.player2_frame += 1
                    elif self.player2_frame == 4 and self.player2_ref.character.hit_type == 'strong':
                        if self.player2_ref.hit_recovery_input:
                            self.player2_frame = 5
                            self.player2_ref.hit_recovery_input = False
                    return

                next_frame = (self.player2_frame + 1) % sprite_count

                # 일반 상태는 단순 순환
                if self.player2_state in ['Idle', 'Walk', 'BackWalk', 'guard']:
                    self.player2_frame = next_frame
                    return

                # 공격 상태에서 애니메이션 완료 시 처리
                if next_frame == 0:  # 애니메이션 한 사이클 완료
                    if self._handle_animation_completion(
                        self.player2_ref, self.player2_state, character_type, False):
                        return

                self.player2_frame = next_frame

        # 연계 가능 시점 체크
        if self.player2_ref and self.player2_ref.is_attacking:
            self._update_combo_availability(
                self.player2_ref, self.player2_state, self.player2_character_type, self.player2_frame)

    def update_player1_position(self, x, y):
        self.player1_x = x
        self.player1_y = y

    def update_player1_direction(self, direction):
        self.player1_dir = direction

    def update_player2_position(self, x, y):
        self.player2_x = x
        self.player2_y = y

    def update_player2_direction(self, direction):
        self.player2_dir = direction

    def render(self):
        """렌더링 - 예외 처리 추가"""
        try:
            # 플레이어1 렌더링 (오른쪽을 바라봄)
            if self.player1_ref:
                character_type = self.player1_character_type
                sprites = self.get_character_sprites(character_type)

                # 캐릭터별 y 오프셋 적용
                y_offset = self.character_y_offsets.get(character_type, 0)
                adjusted_y1 = self.player1_y + y_offset

                if sprites and self.player1_state in sprites:
                    sprite_list = sprites[self.player1_state]
                    if sprite_list and len(sprite_list) > 0:
                        frame = self.player1_frame % len(sprite_list)
                        # 1.5배 스케일링하여 렌더링
                        sprite_list[frame].draw(self.player1_x, adjusted_y1,
                                              sprite_list[frame].w * self.scale_factor,
                                              sprite_list[frame].h * self.scale_factor)

            # 플레이어2 렌더링 (왼쪽을 바라봄)
            if self.player2_ref:
                character_type = self.player2_character_type
                sprites = self.get_character_sprites(character_type)

                # 캐릭터별 y 오프셋 적용
                y_offset = self.character_y_offsets.get(character_type, 0)
                adjusted_y2 = self.player2_y + y_offset

                if sprites and self.player2_state in sprites:
                    sprite_list = sprites[self.player2_state]
                    if sprite_list and len(sprite_list) > 0:
                        frame = self.player2_frame % len(sprite_list)
                        # 왼쪽을 바라보도록 좌우 반전하면서 1.5배 스케일링
                        sprite_list[frame].composite_draw(0, 'h', self.player2_x, adjusted_y2,
                                                        sprite_list[frame].w * self.scale_factor,
                                                        sprite_list[frame].h * self.scale_factor)
        except Exception as e:
            print(f"Warning: Sprite rendering failed: {e}")

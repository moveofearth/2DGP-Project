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

        # 고정된 애니메이션 재생 시간 (초) - config.py 기준
        self.animation_durations = {
            'Idle': 1.0,           # 1초 동안 재생
            'Walk': 0.8,           # 0.8초 동안 재생
            'BackWalk': 0.8,       # 0.8초 동안 재생
            'fastMiddleATK': 0.6,  # Fast 공격: 0.6초
            'fastLowerATK': 0.4,   # Fast 공격: 0.4초
            'fastUpperATK': 0.6,   # Fast 공격: 0.6초
            'strongMiddleATK': 0.9, # Strong 공격: 0.9초
            'strongUpperATK': 1.8,  # Strong 공격: 1.8초 (12프레임)
            'strongLowerATK': 1.35, # Strong 공격: 1.35초 (9프레임)
            'rageSkill': 1.0,      # Rage 스킬: 1초 (18프레임)
            # 'hit'는 이후 guard와 동일하게 맞추기 위해 임시값 제거
            'hit': 0.3,
            'guard': 0.9,          # 가드: 0.9초 (2프레임을 천천히 재생)
            # 연계 공격들
            'fastMiddleATK2': 0.6,
            'fastMiddleATK3': 0.6,
            'strongMiddleATK2': 1.2,
            'strongUpperATK2': 0.75,
        }
        # hit 재생시간을 guard와 동일하게 강제 (guard 시간 변경 시 자동 동기화)
        self.animation_durations['hit'] = self.animation_durations.get('guard', self.animation_durations.get('hit', 0.3))

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
                'strongLowerATK': [pico2d.load_image(str(base_path / 'thief' / 'strongLowerATK' / f'{i}.png')) for i in range(4)],
                'hit': [pico2d.load_image(str(base_path / 'priest' / 'hit' / f'{i}.png')) for i in range(6)],  # priest 공유
                'guard': [pico2d.load_image(str(base_path / 'priest' / 'guard' / f'{i}.png')) for i in range(2)]  # priest 공유
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
                'fastUpperATK': [pico2d.load_image(str(base_path / 'fighter' / 'fastUpperATK' / f'{i}.png')) for i in range(6)],  # 0~5
                'hit': [pico2d.load_image(str(base_path / 'priest' / 'hit' / f'{i}.png')) for i in range(6)],  # priest 공유
                'guard': [pico2d.load_image(str(base_path / 'priest' / 'guard' / f'{i}.png')) for i in range(2)]  # priest 공유
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

        # hit 상태 처리 - 완전한 상태 초기화
        if state == 'hit':
            # hit 애니메이션이 완료되면 hit 상태 완전 초기화
            player_ref.reset_hit_state()
            # SpriteManager 상태도 Idle로 변경
            if is_player1:
                self.player1_state = 'Idle'
                self.player1_frame = 0
                self.frame_timer = 0.0
            else:
                self.player2_state = 'Idle'
                self.player2_frame = 0
                self.player2_frame_timer = 0.0
            print(f"Player {'1' if is_player1 else '2'} hit animation completed - reset to Idle")
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
                    self.frame_timer = 0.0
                else:
                    self.player2_state = next_state
                    self.player2_frame = 0
                    self.player2_frame_timer = 0.0

                # 연계로 새로운 공격이 시작되므로 타격 플래그 초기화
                player_ref.state = next_state
                # 한 공격당 한 번만 타격 처리되도록 리셋
                if hasattr(player_ref, 'reset_attack_hit_flag'):
                    player_ref.reset_attack_hit_flag()
                # 중앙 프레임 기반 히트 판정을 위해 처리 플래그 초기화
                if hasattr(player_ref, 'can_process_hit'):
                    player_ref.can_process_hit = False
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

    def _get_frame_time_for_state(self, state, sprite_count):
        """상태와 스프라이트 개수에 따른 프레임 시간 반환 (고정 재생 시간 기준)"""
        total_duration = self.animation_durations.get(state, 1.0)  # 기본 1초

        if sprite_count > 0:
            return total_duration / sprite_count
        else:
            return 0.1  # 기본값

    def update_player1_state(self, new_state, deltaTime):
        # 캐릭터 타입 변경 감지
        if self.player1_ref:
            current_character_type = self.player1_ref.get_character_type()
            if current_character_type != self.player1_character_type:
                self.player1_character_type = current_character_type
                self.player1_frame = 0
                self.frame_timer = 0.0
                print(f"Player1 character changed to: {current_character_type}")

        # 가드 애니메이션 리셋 체크 (상태 변경과 별도로)
        if (self.player1_ref and self.player1_state == 'guard' and
            new_state == 'guard' and self.player1_ref.should_reset_guard_animation()):
            print("Player1 guard animation reset - extending guard")
            self.player1_frame = 0
            self.frame_timer = 0.0

        # 상태가 변경되면 프레임을 0으로 리셋
        if self.player1_state != new_state:
            print(f"Player1 state changed: {self.player1_state} -> {new_state}")
            self.player1_state = new_state
            self.player1_frame = 0
            self.frame_timer = 0.0
            # 새로운 공격 시작 시 타격 플래그 리셋
            if self.player1_ref and 'ATK' in new_state:
                # 공격 시작 시 기존의 타격 처리 플래그들 초기화
                self.player1_ref.reset_attack_hit_flag()
                self.player1_ref.can_process_hit = False

        character_type = self.player1_character_type
        sprites = self.get_character_sprites(character_type)

        if sprites and self.player1_state in sprites:
            sprite_count = len(sprites[self.player1_state])
            # 스프라이트 개수에 따라 프레임 시간 계산
            # 기본 프레임 시간 계산
            current_frame_time = self._get_frame_time_for_state(self.player1_state, sprite_count)
            # hit 상태는 guard와 같은 전체 재생시간으로 고정
            if self.player1_state == 'hit':
                total_hit_duration = self.animation_durations.get('guard', self.animation_durations.get('hit', 0.3))
                current_frame_time = (total_hit_duration / sprite_count) if sprite_count > 0 else current_frame_time

            # 프레임 애니메이션 업데이트
            self.frame_timer += deltaTime
            if self.frame_timer >= current_frame_time:
                self.frame_timer = 0.0

                # 공격 애니메이션 절반 지점에서 타격 처리 활성화
                if self.player1_ref and 'ATK' in self.player1_state:
                    # 히트 허용: 정확한 중앙 프레임(애니메이션의 1/2 지점)일 때만 허용
                    center = sprite_count // 2
                    # 중앙 프레임과 일치할 때만 타격 처리 허용, 그렇지 않으면 비허용
                    self.player1_ref.can_process_hit = (self.player1_frame == center)

                # hit 상태 특별 처리 - airborne과 down 타입 추가
                if self.player1_state == 'hit' and self.player1_ref:
                    if self.player1_ref.character.hit_type == 'fast':
                        # fast 공격: 프레임 0->1 후 바로 완료
                        if self.player1_frame < 1:
                            self.player1_frame += 1
                        else:
                            # fast hit 애니메이션 완료
                            self._handle_animation_completion(self.player1_ref, 'hit', character_type, True)
                    elif self.player1_ref.character.hit_type == 'strong':
                        # strong 공격: 프레임 0->1->2->3->4 후 기상 대기
                        if self.player1_frame < 4:
                            self.player1_frame += 1
                            # 4번째 프레임에 도달하면 기상 가능 상태로 설정
                            if self.player1_frame == 4:
                                self.player1_ref.character.can_get_up = True
                                print("Player1 can now get up (frame 4)")
                        elif self.player1_frame == 4:
                            # 기상 입력 체크 - 프레임 4에서 대기
                            if self.player1_ref.hit_recovery_input:
                                self.player1_frame = 5  # 기상 프레임
                                self.player1_ref.hit_recovery_input = False
                                print("Player1 getting up!")
                            # 프레임 4에서 대기 (기상 입력 대기)
                        elif self.player1_frame == 5:
                            # 기상 애니메이션 완료
                            self._handle_animation_completion(self.player1_ref, 'hit', character_type, True)
                    elif self.player1_ref.character.hit_type == 'airborne':
                        # 공중에 뜬 상태 - 프레임 0에서 고정, 착지할 때까지 대기
                        self.player1_frame = 0  # 공중에서는 첫 번째 프레임 유지
                        if self.player1_ref.is_grounded and self.player1_ref.character.hit_type == 'down':
                            # 착지 후 down 상태가 되면 프레임 4로 변경
                            self.player1_frame = 4
                            print("Player1 landed - now in down state")
                    elif self.player1_ref.character.hit_type == 'down':
                        # down 상태: 바닥에 떨어진 후 기상 대기
                        if self.player1_frame < 4:
                            self.player1_frame = 4  # down 프레임으로 즉시 이동
                        elif self.player1_frame == 4:
                            # 기상 입력 체크
                            if self.player1_ref.hit_recovery_input:
                                self.player1_frame = 5  # 기상 프레임
                                self.player1_ref.hit_recovery_input = False
                                print("Player1 getting up from down state!")
                        elif self.player1_frame == 5:
                            # 기상 애니메이션 완료
                            self._handle_animation_completion(self.player1_ref, 'hit', character_type, True)
                    return

                next_frame = (self.player1_frame + 1) % sprite_count

                # 일반 상태는 단순 순환, 단 guard는 한 번만 재생
                if self.player1_state in ['Idle', 'Walk', 'BackWalk']:
                    self.player1_frame = next_frame
                    return
                elif self.player1_state == 'guard':
                    # guard는 2프레임을 순차적으로 재생하고 마지막 프레임에서 완료 처리
                    if self.player1_frame < sprite_count - 1:
                        # 아직 마지막 프레임이 아니면 다음 프레임으로
                        self.player1_frame = next_frame
                        return
                    else:
                        # 마지막 프레임에서 완료 처리 (단, 가드가 연장되지 않았을 때만)
                        if self.player1_ref and self.player1_ref.is_guarding:
                            # 추가 공격이 들어와서 가드가 연장되는지 체크
                            if hasattr(self.player1_ref, 'guard_animation_reset') and self.player1_ref.guard_animation_reset:
                                # 가드 연장 - 애니메이션을 처음부터 다시 시작
                                print("Player1 guard extended - restarting animation")
                                self.player1_frame = 0
                                self.frame_timer = 0.0
                                self.player1_ref.guard_animation_reset = False
                                return
                            else:
                                # 정상적인 가드 완료
                                self.player1_ref.is_guarding = False
                                # 상태를 확실히 Idle로 전환
                                self.player1_ref.state = 'Idle'
                                self.player1_ref.character.state = 'Idle'
                                self.player1_state = 'Idle'
                                self.player1_frame = 0
                                self.frame_timer = 0.0  # 타이머 리셋
                                print("Player1 guard animation completed - transitioning to Idle")
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

        # 가드 애니메이션 리셋 체크 (상태 변경과 별도로)
        if (self.player2_ref and self.player2_state == 'guard' and
            new_state == 'guard' and self.player2_ref.should_reset_guard_animation()):
            print("Player2 guard animation reset - extending guard")
            self.player2_frame = 0
            self.player2_frame_timer = 0.0

        # 상태가 변경되면 프레임을 0으로 리셋
        if self.player2_state != new_state:
            print(f"Player2 state changed: {self.player2_state} -> {new_state}")
            self.player2_state = new_state
            self.player2_frame = 0
            self.player2_frame_timer = 0.0
            # 새로운 공격 시작 시 타격 플래그 리셋
            if self.player2_ref and 'ATK' in new_state:
                # 공격 시작 시 기존의 타격 처리 플래그들 초기화
                self.player2_ref.reset_attack_hit_flag()
                self.player2_ref.can_process_hit = False

        character_type = self.player2_character_type
        sprites = self.get_character_sprites(character_type)

        if sprites and self.player2_state in sprites:
            sprite_count = len(sprites[self.player2_state])
            # 스프라이트 개수에 따라 프레임 시간 계산
            # 기본 프레임 시간 계산
            current_frame_time = self._get_frame_time_for_state(self.player2_state, sprite_count)
            # hit 상태는 guard와 같은 전체 재생시간으로 고정
            if self.player2_state == 'hit':
                total_hit_duration = self.animation_durations.get('guard', self.animation_durations.get('hit', 0.3))
                current_frame_time = (total_hit_duration / sprite_count) if sprite_count > 0 else current_frame_time

            # 프레임 애니메이션 업데이트
            self.player2_frame_timer += deltaTime
            if self.player2_frame_timer >= current_frame_time:
                self.player2_frame_timer = 0.0

                # 공격 애니메이션 절반 지점에서 타격 처리 활성화
                if self.player2_ref and 'ATK' in self.player2_state:
                    # 히트 허용: 정확한 중앙 프레임(애니메이션의 1/2 지점)일 때만 허용
                    center = sprite_count // 2
                    # 중앙 프레임과 일치할 때만 타격 처리 허용, 그렇지 않으면 비허용
                    self.player2_ref.can_process_hit = (self.player2_frame == center)

                # hit 상태 특별 처리 - airborne과 down 타입 추가
                if self.player2_state == 'hit' and self.player2_ref:
                    if self.player2_ref.character.hit_type == 'fast':
                        # fast 공격: 프레임 0->1 후 바로 완료
                        if self.player2_frame < 1:
                            self.player2_frame += 1
                        else:
                            # fast hit 애니메이션 완료
                            self._handle_animation_completion(self.player2_ref, 'hit', character_type, False)
                    elif self.player2_ref.character.hit_type == 'strong':
                        # strong 공격: 프레임 0->1->2->3->4 후 기상 대기
                        if self.player2_frame < 4:
                            self.player2_frame += 1
                            # 4번째 프레임에 도달하면 기상 가능 상태로 설정
                            if self.player2_frame == 4:
                                self.player2_ref.character.can_get_up = True
                                print("Player2 can now get up (frame 4)")
                        elif self.player2_frame == 4:
                            # 기상 입력 체크 - 프레임 4에서 대기
                            if self.player2_ref.hit_recovery_input:
                                self.player2_frame = 5  # 기상 프레임
                                self.player2_ref.hit_recovery_input = False
                                print("Player2 getting up!")
                            # 프레임 4에서 대기 (기상 입력 대기)
                        elif self.player2_frame == 5:
                            # 기상 애니메이션 완료
                            self._handle_animation_completion(self.player2_ref, 'hit', character_type, False)
                    elif self.player2_ref.character.hit_type == 'airborne':
                        # 공중에 뜬 상태 - 프레임 0에서 고정, 착지할 때까지 대기
                        self.player2_frame = 0  # 공중에서는 첫 번째 프레임 유지
                        if self.player2_ref.is_grounded and self.player2_ref.character.hit_type == 'down':
                            # 착지 후 down 상태가 되면 프레임 4로 변경
                            self.player2_frame = 4
                            print("Player2 landed - now in down state")
                    elif self.player2_ref.character.hit_type == 'down':
                        # down 상태: 바닥에 떨어진 후 기상 대기
                        if self.player2_frame < 4:
                            self.player2_frame = 4  # down 프레임으로 즉시 이동
                        elif self.player2_frame == 4:
                            # 기상 입력 체크
                            if self.player2_ref.hit_recovery_input:
                                self.player2_frame = 5  # 기상 프레임
                                self.player2_ref.hit_recovery_input = False
                                print("Player2 getting up from down state!")
                        elif self.player2_frame == 5:
                            # 기상 애니메이션 완료
                            self._handle_animation_completion(self.player2_ref, 'hit', character_type, False)
                    return

                next_frame = (self.player2_frame + 1) % sprite_count

                # 일반 상태는 단순 순환, 단 guard는 한 번만 재생
                if self.player2_state in ['Idle', 'Walk', 'BackWalk']:
                    self.player2_frame = next_frame
                    return
                elif self.player2_state == 'guard':
                    # guard는 2프레임을 순차적으로 재생하고 마지막 프레임에서 완료 처리
                    if self.player2_frame < sprite_count - 1:
                        # 아직 마지막 프레임이 아니면 다음 프레임으로
                        self.player2_frame = next_frame
                        return
                    else:
                        # 마지막 프레임에서 완료 처리 (단, 가드가 연장되지 않았을 때만)
                        if self.player2_ref and self.player2_ref.is_guarding:
                            # 추가 공격이 들어와서 가드가 연장되는지 체크
                            if hasattr(self.player2_ref, 'guard_animation_reset') and self.player2_ref.guard_animation_reset:
                                # 가드 연장 - 애니메이션을 처음부터 다시 시작
                                print("Player2 guard extended - restarting animation")
                                self.player2_frame = 0
                                self.player2_frame_timer = 0.0
                                self.player2_ref.guard_animation_reset = False
                                return
                            else:
                                # 정상적인 가드 완료
                                self.player2_ref.is_guarding = False
                                # 상태를 확실히 Idle로 전환
                                self.player2_ref.state = 'Idle'
                                self.player2_ref.character.state = 'Idle'
                                self.player2_state = 'Idle'
                                self.player2_frame = 0
                                self.player2_frame_timer = 0.0  # 타이머 리셋
                                print("Player2 guard animation completed - transitioning to Idle")
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

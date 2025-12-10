from Character.character import Character
import pico2d
import config
from handle_collision import CollisionHandler
import pathlib


class Player:

    def __init__(self, player_side='left', character_type=None):  # player_side: 'left' 또는 'right'
        # player_side에 따른 초기 설정
        if player_side == 'left':
            self.x = config.windowWidth * 0.35  # 화면 왼쪽 35% 위치
            self.player_side = 'left'
            self.dir = 1  # 왼쪽 플레이어는 오른쪽(상대방)을 바라봄
            self.facing_right = True
            if character_type is None:
                character_type = 'thief'
        elif player_side == 'right':
            self.x = config.windowWidth * 0.65  # 화면 오른쪽 65% 위치
            self.player_side = 'right'
            self.dir = -1  # 오른쪽 플레이어는 왼쪽(상대방)을 바라봄
            self.facing_right = False
            if character_type is None:
                character_type = 'priest'
        else:
            raise ValueError("player_side must be 'left' or 'right'")

        self.y = config.GROUND_Y
        self.character = Character(character_type)  # Character 인스턴스 추가
        self.character.x, self.character.y = self.x, self.y  # 캐릭터 위치 동기화
        self.hp = 100  # HP 추가
        self.max_hp = 100  # 최대 HP

        # 물리 변수 추가
        self.velocity_y = 0.0  # Y방향 속도
        self.velocity_x = 0.0  # X방향 속도 (포물선 운동용)
        self.is_grounded = True  # 지면에 있는지 체크
        self.gravity = config.GRAVITY  # 중력 가속도

        self.prev_x = self.x
        self.state = 'Idle'  # Idle, Walk, BackWalk
        self.position_state = 'Middle'  # High, Middle, Low 상태 추가
        self.is_attacking = False  # 공격 중인지 체크
        self.is_hit = False  # 피격 중인지 체크
        self.hit_recovery_input = False  # 기상 입력 플래그
        self.can_combo = False  # 연계 가능 상태
        self.combo_reserved = False  # 연계 공격 예약 상태

        # 가드 상태 관련 속성 추가
        self.is_guarding = False  # 가드 중인지 체크
        # guard_timer와 guard_duration 제거 - 애니메이션으로 제어

        # 공격 타격 처리 관련 속성 추가
        self.attack_hit_processed = False  # 현재 공격의 타격 처리 완료 여부
        # SpriteManager와 연동되는 타격 허용 플래그 초기화 (프레임 기반 히트 판정)
        self.can_process_hit = False

        # 캐릭터별 사용 가능한 공격 정의
        self.available_attacks = {
            'priest': ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK', 'strongLowerATK', 'rageSkill', 'guard'],
            'thief': ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK', 'strongLowerATK', 'guard'],
            'fighter': ['fastMiddleATK', 'fastLowerATK', 'fastUpperATK', 'strongMiddleATK', 'strongLowerATK', 'strongUpperATK', 'guard']
        }

        # 이동 속도 조정
        self.move_speed_multiplier = 1.0  # 이동 속도 배율

        # 가드 후 즉시 공격 가능 창 (초단위)
        self.guard_counter_window = 0.25  # 가드 후 0.25초 동안 반격 가능
        self.guard_counter_timer = 0.0
        self.can_attack_after_guard = False

        # 사운드 초기화
        self.hit_sound = None
        self.swoosh_sound = None
        self.attack_sound_played = False  # 공격 사운드 재생 여부 플래그

    def get_character_type(self):
        """현재 캐릭터 타입 반환"""
        return self.character.get_character_type()

    def can_use_attack(self, attack_type):
        """현재 캐릭터가 해당 공격을 사용할 수 있는지 확인"""
        character_type = self.get_character_type()
        return attack_type in self.available_attacks.get(character_type, [])

    def is_attack_state(self):
        """현재 상태가 공격 상태인지 확인"""
        attack_states = ['fastMiddleATK', 'fastMiddleATK2', 'fastMiddleATK3', 'strongMiddleATK', 'strongMiddleATK2', 'strongUpperATK', 'strongUpperATK2', 'strongLowerATK', 'fastLowerATK', 'fastUpperATK', 'rageSkill']
        return self.state in attack_states

    def get_move_speed(self):
        """현재 캐릭터의 이동속도 반환 (조정된 속도)"""
        base_speed = self.character.get_move_speed()
        return base_speed * self.move_speed_multiplier

    def initialize(self):
        self.character.initialize()  # Character 초기화
        # Character의 HP와 max_hp 동기화
        self.character.max_hp = self.max_hp
        self.character.hp = self.max_hp
        # player_side에 따른 초기화
        if self.player_side == 'left':
            self.x = config.windowWidth * 0.3  # 화면 왼쪽 30% 위치
            self.dir = 1  # 왼쪽 플레이어는 오른쪽(상대방)을 바라봄
            self.facing_right = True
            self.hp = self.max_hp
        elif self.player_side == 'right':
            self.x = config.windowWidth * 0.7  # 화면 오른쪽 70% 위치
            self.dir = -1  # 오른쪽 플레이어는 왼쪽(상대방)을 바라봄
            self.facing_right = False
            self.hp = self.max_hp
        self.character.hp = self.hp
        self.y = config.GROUND_Y
        self.is_grounded = True

        # 피격 사운드 로드
        if self.hit_sound is None:
            hit_sound_path = pathlib.Path.cwd() / 'Resources' / 'Sound' / 'hit.wav'
            self.hit_sound = pico2d.load_wav(str(hit_sound_path))
            self.hit_sound.set_volume(32)

        # 공격 사운드 로드
        if self.swoosh_sound is None:
            swoosh_sound_path = pathlib.Path.cwd() / 'Resources' / 'Sound' / 'swoosh.wav'
            self.swoosh_sound = pico2d.load_wav(str(swoosh_sound_path))
            self.swoosh_sound.set_volume(32)

    def change_character(self, character_type):
        """캐릭터 변경"""
        self.character = Character(character_type)
        self.character.x, self.character.y = self.x, self.y
        self.character.hp = self.hp
        self.character.initialize()
        # 상태 초기화
        self.state = 'Idle'
        self.is_attacking = False
        self.is_hit = False
        self.is_guarding = False
        self.can_combo = False
        self.combo_reserved = False

    def apply_gravity(self, deltaTime):
        """중력 적용 - airborne 상태 처리 및 개선된 충돌 처리"""
        if not self.is_grounded:
            # 중력으로 인한 Y방향 속도 감소
            self.velocity_y -= self.gravity * deltaTime
            # 위치 업데이트 (포물선: x, y 둘다)
            old_y = self.y
            self.x += self.velocity_x * deltaTime

            # 공중에서도 화면 경계 체크 (벽을 뚫고 나가지 않도록)
            CollisionHandler.clamp_to_screen(self)

            # 공중 수평 감속(간단한 댐핑) - 초당 약 6의 감속계수로 자연스럽게 줄어듦
            damping_factor = 6.0
            self.velocity_x *= max(0.0, 1.0 - damping_factor * deltaTime)

            self.y += self.velocity_y * deltaTime

            # 그라운드 체크
            if self.y <= config.GROUND_Y:
                self.y = config.GROUND_Y
                self.velocity_y = 0.0
                # 착지하면 수평 속도도 정지
                self.velocity_x = 0.0
                self.is_grounded = True

                # 공중에서 떨어진 후 착지했을 때 특별 처리
                if (self.is_hit and hasattr(self.character, 'hit_type') and
                    self.character.hit_type == 'airborne' and old_y > config.GROUND_Y):
                    # airborne에서 착지 - down 상태로 전환하고 기상 가능하게 설정
                    self.character.hit_type = 'down'  # down 상태로 변경
                    self.character.can_get_up = True
                    self.character.frame = 4  # down 프레임으로 설정
                    print("Player landed and is now down - can get up")

        elif self.y > config.GROUND_Y:
            # 그라운드보다 높은 위치에 있으면 떨어지기 시작
            self.is_grounded = False
            if self.velocity_y == 0:
                self.velocity_y = 0.0

    def jump(self, jump_force=500.0):
        """점프 (필요시 사용)"""
        if self.is_grounded:
            self.velocity_y = jump_force
            self.is_grounded = False

    def check_collision_with_other_player(self, other_player):
        """다른 플레이어와의 충돌 검사 - CollisionHandler 사용"""
        return CollisionHandler.check_player_collision(self, other_player)

    def resolve_collision_with_other_player(self, other_player):
        """다른 플레이어와의 충돌 해결 - CollisionHandler 사용"""
        CollisionHandler.resolve_player_collision(self, other_player)

    def update_position(self, new_x, other_player=None):
        """위치 업데이트 (충돌 검사 포함) - 개선된 충돌 처리 사용"""
        # 이전 위치 저장 (디버깅/롤백용)
        self.prev_x = self.x

        # CollisionHandler의 안전한 이동 사용
        self.x = CollisionHandler.safe_move_player(self, new_x, other_player)



    def start_guard(self):
        """가드 상태 시작 - 피격 시 자동으로 발동"""
        # 공격 중이면 가드 불가 (공격 도중 들어오는 공격은 방어하지 않음)
        if getattr(self, 'is_attacking', False):
            print("Cannot start guard while attacking")
            return

        # 피격 중이면 가드 불가
        if getattr(self, 'is_hit', False):
            print("Cannot start guard while being hit")
            return

        # 이미 가드 중이라면 가드를 연장 (애니메이션 리셋)
        if self.is_guarding:
            print(f"Guard extended! Position: {self.position_state} - Resetting guard animation")
            self.guard_animation_reset = True
            # 반격 창도 연장
            self.guard_counter_timer = self.guard_counter_window
            self.can_attack_after_guard = True
        else:
            self.is_guarding = True
            self.guard_animation_reset = False
            print(f"Auto guard activated! Position: {self.position_state} - Starting guard animation")

            # 가드 시작 시 짧은 반격 창 부여
            self.guard_counter_timer = self.guard_counter_window
            self.can_attack_after_guard = True
            print(f"Guard counter window opened for {self.guard_counter_window} seconds")

        self.state = 'guard'
        # Character 상태도 즉시 동기화
        self.character.state = 'guard'

    def should_reset_guard_animation(self):
        """가드 애니메이션 리셋이 필요한지 확인"""
        if hasattr(self, 'guard_animation_reset') and self.guard_animation_reset:
            self.guard_animation_reset = False  # 플래그 리셋
            return True
        return False

    def update_guard(self, deltaTime):
        """가드 상태 업데이트 - 애니메이션으로 제어됨"""
        # 가드 상태는 spriteManager에서 애니메이션 완료 시 자동으로 해제됨
        # 불필요한 상태 체크 제거
        pass

    def end_guard(self):
        """가드 상태 종료"""
        if self.is_guarding:
            self.is_guarding = False
            if not self.is_attacking and not self.is_hit:
                self.state = 'Idle'
                self.character.state = 'Idle'
            print(f"Guard ended - transitioning to {self.state}")

    def can_guard_against_attack(self, attack_type):
        """공격 타입에 따른 가드 가능 여부 확인"""
        # 공격 중이면 가드 불가 (공격이 들어왔을 때 공격 중이면 방어하지 않음)
        if getattr(self, 'is_attacking', False):
            return False

        # 피격 중일 때도 가드 불가
        if getattr(self, 'is_hit', False):
            return False

        guard_mapping = {
            # 기본 공격
            'fastUpperATK': 'High',
            'strongUpperATK': 'High',
            'fastMiddleATK': 'Middle',
            'strongMiddleATK': 'Middle',
            'fastLowerATK': 'Low',
            'strongLowerATK': 'Low',
            # 연계 공격 (2단, 3단)
            'fastMiddleATK2': 'Middle',
            'fastMiddleATK3': 'Middle',
            'strongMiddleATK2': 'Middle',
            'strongUpperATK2': 'High',
            # rage 스킬은 가드 불가
            'rageSkill': None
        }

        required_position = guard_mapping.get(attack_type)

        # rage 스킬은 가드 불가
        if required_position is None:
            return False

        # 방향키 입력과 공격 타입이 일치해야 가드 성공
        if required_position and self.position_state == required_position:
            return True
        return False

    def get_bb(self):
        """바운딩 박스 좌표 반환 - 방향과 상태에 따라 동적 계산"""
        # down 상태인지 확인
        hit_type = getattr(self.character, 'hit_type', None) if hasattr(self, 'character') else None
        is_down = (hit_type == 'down') or (self.is_hit and not self.is_grounded and hit_type == 'airborne')

        if is_down:
            # down 상태: 누워있으므로 바운딩 박스를 가로로 넓고 세로로 좁게
            bb_width = 70 * 1.5  # 가로로 더 넓게
            bb_height = 25 * 1.5  # 세로로 더 낮게 (바닥에 붙어있음)
            adjusted_x = self.x
            adjusted_y = self.y - (15 * 1.5)  # 바닥에 더 가깝게
        else:
            # 일반 상태: 1.5배 스케일링 적용
            bb_width = 40 * 1.5  # 60
            bb_height = 50 * 1.5  # 75

            # 방향에 따라 x 오프셋 조정
            if self.facing_right:
                # 오른쪽을 바라볼 때: 왼쪽으로 오프셋
                adjusted_x = self.x - (30 * 1.5)
            else:
                # 왼쪽을 바라볼 때: 오른쪽으로 오프셋
                adjusted_x = self.x + (30 * 1.5)

            adjusted_y = self.y - (50 * 1.5)

        return adjusted_x - bb_width, adjusted_y - bb_height, adjusted_x + bb_width, adjusted_y + bb_height

    def get_attack_range_bb(self):
        """공격 범위의 바운딩 박스 반환 (방향에 따라 동적 계산)"""
        my_bb = self.get_bb()

        # 공격 범위 설정
        attack_range = 0

        # priest의 상단 강공격은 특별히 범위가 두 배
        if (self.character.currentCharacter == 'priest' and
            self.state.lower() == 'strongupperatk'):
            attack_range = 200  # priest의 상단 강공격은 200
        elif 'fast' in self.state.lower():
            attack_range = 70  # fast 계열을 70으로 설정
        elif 'strong' in self.state.lower():
            attack_range = 100  # strong 계열을 100으로 설정
        elif 'rage' in self.state.lower():
            attack_range = 70

        if attack_range == 0:
            return None

        # 공격 범위는 상하는 바운딩 박스와 동일하지만,
        # Lower 공격은 아래쪽으로 더 넓은 범위를 가짐 (down 상태 타격용)
        is_lower_attack = 'lower' in self.state.lower()

        if is_lower_attack:
            # Lower 공격은 바닥 근처까지 범위 확장
            # down 상태의 바운딩 박스를 확실히 커버하도록 범위 확대
            range_y1 = config.GROUND_Y - 100  # 더 넓은 범위로 확장 (60 -> 100)
            range_y2 = my_bb[3]
        else:
            # 일반 공격은 바운딩 박스와 동일
            range_y1 = my_bb[1]
            range_y2 = my_bb[3]

        if self.facing_right:
            # 오른쪽을 바라볼 때: 바운딩 박스 오른쪽 끝에서 오른쪽으로 공격
            range_x1 = my_bb[2]  # 바운딩 박스 오른쪽 끝
            range_x2 = range_x1 + attack_range
        else:
            # 왼쪽을 바라볼 때: 바운딩 박스 왼쪽 끝에서 왼쪽으로 공격
            range_x2 = my_bb[0]  # 바운딩 박스 왼쪽 끝
            range_x1 = range_x2 - attack_range

        return range_x1, range_y1, range_x2, range_y2


    def is_in_attack_range(self, other_player):
        """다른 플레이어가 공격 범위 내에 있는지 확인"""
        if not other_player or not self.is_attacking:
            return False

        attack_bb = self.get_attack_range_bb()
        if not attack_bb:
            return False

        other_bb = other_player.get_bb()

        # AABB 충돌 검사
        return (attack_bb[0] < other_bb[2] and attack_bb[2] > other_bb[0] and
                attack_bb[1] < other_bb[3] and attack_bb[3] > other_bb[1])

    def reset_attack_hit_flag(self):
        """새로운 공격 시작 시 타격 플래그 리셋"""
        self.attack_hit_processed = False
        self.attack_sound_played = False

    def can_hit_target(self):
        """타격 처리 가능 여부 확인 (한 공격당 한 번만)"""
        return self.is_attacking and not self.attack_hit_processed

    def mark_attack_hit_processed(self):
        """타격 처리 완료 마킹"""
        self.attack_hit_processed = True

    def is_in_hit_state(self):
        """피격 상태인지 확인 - down 상태 구분"""
        if not self.is_hit:
            return False

        # down 상태는 Lower 공격에 피격될 수 있으므로 특수 처리
        # character의 hit_type을 확인하여 down 상태를 정확히 감지
        hit_type = getattr(self.character, 'hit_type', None) if hasattr(self, 'character') else None

        # down 상태는 피격 상태이지만 Lower 공격에는 반응할 수 있도록
        # 여기서는 단순히 is_hit만 반환 (충돌 체크에서 hit_type으로 추가 판단)
        return True

    def take_damage(self, damage, attack_state='fastMiddleATK', attacker=None):
        """데미지를 받는 메서드 - 공격 상태에 따른 hit 타입 결정"""
        # 현재 airborne 상태인지 체크 (추가 공격 판정용)
        was_airborne = (hasattr(self.character, 'hit_type') and
                       self.character.hit_type == 'airborne' and
                       not self.is_grounded)

        # 공격 상태에 따른 hit 타입 결정
        # 1순위: Lower 계열은 포물선로 띄우기 위해 airborne 취급
        if 'lower' in attack_state.lower():
            attack_type = 'airborne'
        # 2순위: Upper 계열은 상단 판정
        elif 'upper' in attack_state.lower():
            # Upper 계열도 강도에 따라 구분
            if 'strong' in attack_state.lower():
                attack_type = 'strong'
            else:
                attack_type = 'fast'
        # 3순위: Middle 계열은 중단 판정
        elif 'middle' in attack_state.lower():
            # Middle 계열도 강도에 따라 구분
            if 'strong' in attack_state.lower():
                attack_type = 'strong'
            else:
                attack_type = 'fast'
        # 4순위: 기타 공격은 강도만 체크
        elif 'strong' in attack_state.lower():
            attack_type = 'strong'
        else:
            attack_type = 'fast'

        # Character의 take_damage 호출
        self.character.take_damage(damage, attack_type)

        # Player HP 및 상태 동기화
        self.hp = self.character.hp
        self.is_hit = self.character.is_hit
        self.state = 'hit'  # Player 상태도 hit로 설정

        # 피격 사운드 재생
        if self.hit_sound:
            self.hit_sound.play()

        # 포물선 처리: Lower 계열 공격 또는 공중에서 추가 히트
        should_launch = ('lower' in attack_state.lower()) or was_airborne

        if should_launch:
            # 세기 결정
            if 'lower' in attack_state.lower():
                # Lower 계열 공격 (지상에서 띄우기 - 위로)
                if 'strong' in attack_state.lower():
                    vy = 640.0
                    vx_mag = 300.0
                else:
                    vy = 480.0
                    vx_mag = 200.0
                # x 가속도를 80%로 감소
                vx_mag = vx_mag * 0.8
            else:
                # 공중에서 추가 히트 (에어 콤보)
                if 'strong' in attack_state.lower():
                    # 강공격: 뒤로 크게 날아가면서 위로도 튀어오름
                    vy = 400.0  # 수직 속도 증가 (200 -> 400)
                    vx_mag = 450.0  # 수평 속도 크게 (뒤로 날아가는 효과)
                elif 'fast' in attack_state.lower():
                    # 빠른 공격: 위로 올라가며 약간 밀림
                    vy = 350.0
                    vx_mag = 180.0
                else:
                    # 기타 공격
                    vy = 400.0
                    vx_mag = 200.0
                # 공중 콤보는 x 가속도 감소 없음 (그대로 유지)

            # 공격자 위치를 참고해 밀려나는 방향 결정 (공격자 기준 밖으로)
            if attacker and hasattr(attacker, 'x'):
                if attacker.x < self.x:
                    self.velocity_x = vx_mag
                else:
                    self.velocity_x = -vx_mag
            else:
                # 공격자 정보 없으면 기본으로 오른쪽으로 밀려나게 설정
                self.velocity_x = vx_mag if self.x < config.windowWidth / 2 else -vx_mag

            self.velocity_y = vy
            self.is_grounded = False
            # 살짝 띄워 충돌/착지 로직을 명확히
            if not was_airborne:
                self.y += 5

            hit_type = "AIRBORNE COMBO" if was_airborne else "LAUNCH"
            combo_type = " (KNOCKBACK)" if was_airborne and 'strong' in attack_state.lower() else ""
            print(f"Player {hit_type}{combo_type} by {attack_state}! vx:{self.velocity_x}, vy:{self.velocity_y}")

        # 공격 및 가드 상태 초기화 (피격 시 모든 행동 중단)
        # 공격을 받은 순간 현재 진행중인 공격을 취소하고,
        # 해당 공격은 더 이상 타격 판정을 발생시키지 않도록 모든 관련 플래그를 초기화한다.
        self.is_attacking = False
        # 이미 현재 공격에 대한 타격 처리가 끝난 것으로 마킹하여 이후 판정에서 제외
        self.attack_hit_processed = True
        # SpriteManager가 설정하는 타격 허용 플래그도 즉시 비활성화
        self.can_process_hit = False
        self.is_guarding = False
        self.can_combo = False
        self.combo_reserved = False

        print(f"Player took {damage} damage, HP: {self.hp}, hit_type: {attack_type}")
        return self.hp

    def reset_hit_state(self):
        """hit 상태 완전 초기화"""
        # hit 상태 및 공격 관련 플래그 안전 초기화
        self.is_hit = False
        self.character.reset_hit_state()
        # 공격 관련 플래그도 확실히 비활성화
        self.is_attacking = False
        self.can_process_hit = False
        self.attack_hit_processed = True
        self.can_combo = False
        self.combo_reserved = False
        if self.state == 'hit':
            self.state = 'Idle'
        print("Player hit state reset to normal (attack cancelled and flags cleared)")

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False, char_change_input=None, other_player=None, position_state='Middle', getup_input=False):
        # 위치 상태 업데이트
        self.position_state = position_state

        # 가드 반격 창 타이머 감소
        if self.guard_counter_timer > 0.0:
            self.guard_counter_timer = max(0.0, self.guard_counter_timer - deltaTime)
            if self.guard_counter_timer == 0.0:
                self.can_attack_after_guard = False
                print("Guard counter window closed")

        # 가드 상태 업데이트 (빈 함수)
        self.update_guard(deltaTime)

        # 캐릭터 타입 변경 처리 (공격 중이 아니고 가드 중이 아니고 피격 중이 아닐 때만)
        if char_change_input and not self.is_attacking and not self.is_guarding and not self.is_hit and char_change_input in ['priest', 'thief', 'fighter']:
            current_type = self.get_character_type()
            if current_type != char_change_input:
                self.set_character_type(char_change_input)
                return

        # 중력 적용 (항상) - airborne 상태 처리 포함
        self.apply_gravity(deltaTime)

        # hit 상태 동기화 - Character와 Player 상태 일치 확인
        if self.character.is_hit != self.is_hit:
            self.is_hit = self.character.is_hit
            if self.is_hit and self.state != 'hit':
                self.state = 'hit'
            elif not self.is_hit and self.state == 'hit':
                self.state = 'Idle'

        # 가드 중일 때 공격키 입력으로 가드 취소 후 즉시 공격 허용
        if self.is_guarding and not self.is_attacking and atk_input:
            if self.can_use_attack(atk_input):
                # 가드 상태 완전 해제
                self.is_guarding = False
                self.can_attack_after_guard = False
                self.guard_counter_timer = 0.0
                if hasattr(self, 'guard_animation_reset'):
                    self.guard_animation_reset = False

                # 즉시 공격 시작
                self.state = atk_input
                self.character.state = atk_input  # Character 상태 즉시 동기화
                self.is_attacking = True
                self.reset_attack_hit_flag()

                # 연계 가능 설정
                if atk_input in ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK']:
                    self.can_combo = True
                else:
                    self.can_combo = False

                self.combo_reserved = False

                print(f"Guard canceled by attack input -> immediate attack: {atk_input}")
                return
            else:
                print(f"Cannot use attack {atk_input} for current character")

        # 가드 중이면 다른 행동 불가 - 상태 강제 동기화
        if self.is_guarding:
            # 가드 중에는 상태가 'guard'로 고정되어야 함
            if self.state != 'guard':
                self.state = 'guard'
            if self.character.state != 'guard':
                self.character.state = 'guard'
            # 이동 등 다른 행동은 제한
            return

        # hit 상태일 때 기상 입력 처리 - airborne과 down 상태 구분
        if self.is_hit and self.character.can_get_up:
            # down 상태 (바닥에 떨어진 후)에서만 기상 가능
            if (hasattr(self.character, 'hit_type') and
                self.character.hit_type == 'down' and self.is_grounded):
                # 방향키 입력이 있으면 기상 시도
                if getup_input:
                    if self.character.try_get_up():
                        self.hit_recovery_input = True
                        print(f"Player attempting to get up from down state!")
                        return
            # strong 공격의 일반적인 기상 처리
            elif (hasattr(self.character, 'hit_type') and
                  self.character.hit_type == 'strong'):
                # 방향키 입력이 있으면 기상 시도
                if getup_input:
                    if self.character.try_get_up():
                        self.hit_recovery_input = True
                        print(f"Player attempting to get up! Current frame: {self.character.frame}")
                        return

        # hit 상태가 아닐 때만 일반 행동 처리
        if not self.is_hit:
            # 연계 공격 처리 (우선순위 1) - 정확한 키 조합으로만 발동
            if combo_input and self.can_combo and not self.combo_reserved:
                # combo_input이 연계 타입을 반환 (예: 'fastMiddleATK_combo', 'strongMiddleATK_combo', 'strongUpperATK_combo')
                # 현재 상태와 맞는 연계인지 확인
                if (self.state == 'fastMiddleATK' and combo_input == 'fastMiddleATK_combo') or \
                   (self.state == 'fastMiddleATK2' and combo_input == 'fastMiddleATK_combo') or \
                   (self.state == 'strongMiddleATK' and combo_input == 'strongMiddleATK_combo') or \
                   (self.state == 'strongUpperATK' and combo_input == 'strongUpperATK_combo'):
                    self.combo_reserved = True
                    print(f"Combo reserved for {self.get_character_type()}: {self.state} -> {combo_input}")
                    return

            # 새로운 공격 입력 처리 (공격 중이 아닐 때만)
            if not self.is_attacking and atk_input:
                # 캐릭터별 공격 제한 확인
                if self.can_use_attack(atk_input):
                    # 반격 창 동안 가드 중이면 가드 해제하고 즉시 공격 허용
                    if self.is_guarding and self.can_attack_after_guard:
                        self.is_guarding = False
                        self.can_attack_after_guard = False
                        self.guard_counter_timer = 0.0
                        print("Guard canceled to perform immediate attack")

                    self.state = atk_input
                    self.is_attacking = True
                    self.reset_attack_hit_flag()  # 새 공격 시작 시 타격 플래그 리셋

                    # 연계 가능한 공격 설정
                    if atk_input in ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK']:
                        self.can_combo = True
                    else:
                        self.can_combo = False

                    self.combo_reserved = False
                    print(f"Starting attack: {atk_input}")
                    return

            # 이동 처리 - 상대 플레이어의 위치에 따라 동적으로 Walk/BackWalk 결정
            if not self.is_attacking and not self.is_guarding and not self.is_hit and self.is_grounded:
                move_speed = self.get_move_speed()

                # 상대방이 내 오른쪽에 있는지 왼쪽에 있는지 판단
                opponent_on_right = other_player and other_player.x > self.x

                if move_input == 'right':
                    # 오른쪽으로 이동
                    if opponent_on_right:
                        # 상대가 오른쪽에 있으면 Walk (접근)
                        new_x = self.x + move_speed * deltaTime
                        self.state = 'Walk'
                        self.facing_right = True
                        self.dir = 1
                    else:
                        # 상대가 왼쪽에 있으면 BackWalk (후퇴) - Walk와 동일한 속도
                        new_x = self.x + move_speed * deltaTime
                        self.state = 'BackWalk'
                        self.facing_right = False
                        self.dir = -1
                    self.update_position(new_x, other_player)

                elif move_input == 'left':
                    # 왼쪽으로 이동
                    if opponent_on_right:
                        # 상대가 오른쪽에 있으면 BackWalk (후퇴) - Walk와 동일한 속도
                        new_x = self.x - move_speed * deltaTime
                        self.state = 'BackWalk'
                        self.facing_right = True
                        self.dir = 1
                    else:
                        # 상대가 왼쪽에 있으면 Walk (접근)
                        new_x = self.x - move_speed * deltaTime
                        self.state = 'Walk'
                        self.facing_right = False
                        self.dir = -1
                    self.update_position(new_x, other_player)

                elif not move_input:
                    self.state = 'Idle'
                    # Idle 상태에서도 상대방을 바라보도록 방향 업데이트
                    if opponent_on_right:
                        self.facing_right = True
                        self.dir = 1
                    else:
                        self.facing_right = False
                        self.dir = -1

        # 캐릭터 위치 및 상태 동기화
        self.character.x, self.character.y = self.x, self.y
        if not self.is_hit and not self.is_guarding:  # hit 상태나 가드 상태가 아닐 때만 상태 동기화
            self.character.state = self.state
        elif self.is_hit:  # hit 상태일 때는 강제로 hit 상태 유지
            self.character.state = 'hit'
        self.character.hp = self.hp

        # Character 업데이트
        self.character.update(deltaTime)

    def set_character_type(self, character_type):
        """캐릭터 타입 변경"""
        if character_type in ['priest', 'thief', 'fighter']:
            self.character.set_character_type(character_type)
            # 모든 상태 초기화
            self.is_attacking = False
            self.is_guarding = False
            self.is_hit = False  # hit 상태도 초기화
            self.can_combo = False
            self.combo_reserved = False
            self.state = 'Idle'
            # Character 상태도 동기화
            self.character.state = 'Idle'
            self.character.is_hit = False

    def heal(self, amount):
        """체력을 회복하는 메서드"""
        self.hp = min(self.max_hp, self.hp + amount)
        self.character.hp = self.hp
        return self.hp

    def is_alive(self):
        """생존 여부 확인"""
        return self.hp > 0

    def get_hp(self):
        """현재 HP 반환"""
        return self.hp

    def get_hp_percentage(self):
        """HP 퍼센테이지 반환 (0.0 ~ 1.0)"""
        return self.hp / self.max_hp

    def render(self):
        # 바운딩 박스 및 공격 범위 박스 그리기 (F1 키로 토글)
        if config.SHOW_BOUNDING_BOX:
            # 피격 박스 (빨간색)
            pico2d.draw_rectangle(*self.get_bb())

            # 공격 범위 박스 (초록색, 공격 중일 때만)
            if self.is_attacking:
                attack_bb = self.get_attack_range_bb()
                if attack_bb:
                    # 공격 범위 박스 그리기
                    pico2d.draw_rectangle(*attack_bb)

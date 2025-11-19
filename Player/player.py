from Character.character import Character
import pico2d
import pathlib
import config


class Player:

    def __init__(self, x=600, y=450, character_type='priest'):  # 이미 스케일링된 위치
        self.x, self.y = x, config.GROUND_Y  # y를 그라운드로 설정
        self.character = Character(character_type)  # Character 인스턴스 추가
        self.character.x, self.character.y = self.x, self.y  # 캐릭터 위치 동기화
        self.hp = 100  # HP 추가
        self.max_hp = 100  # 최대 HP

        # 물리 변수 추가
        self.velocity_y = 0.0  # Y방향 속도
        self.is_grounded = True  # 지면에 있는지 체크
        self.gravity = config.GRAVITY  # 중력 가속도

        # 이전 위치 저장 (충돌 시 되돌리기 위해)
        self.prev_x = x

        self.dir = -1  # 항상 오른쪽을 바라보도록 -1로 고정
        self.state = 'Idle'  # Idle, Walk, BackWalk
        self.position_state = 'Middle'  # High, Middle, Low 상태 추가
        self.is_attacking = False  # 공격 중인지 체크
        self.is_hit = False  # 피격 중인지 체크
        self.hit_recovery_input = False  # 기상 입력 플래그
        self.can_combo = False  # 연계 가능 상태
        self.combo_reserved = False  # 연계 공격 예약 상태

        # 가드 상태 관련 속성 추가
        self.is_guarding = False  # 가드 중인지 체크
        self.guard_timer = 0.0  # 가드 지속 시간
        self.guard_duration = 0.05  # 가드 지속 시간 (0.05초)

        # 공격 타격 처리 관련 속성 추가
        self.attack_hit_processed = False  # 현재 공격의 타격 처리 완료 여부

        # pico2d 폰트 로드 - 개선된 예외 처리
        self.font = None
        self._load_font()

        # 캐릭터별 사용 가능한 공격 정의
        self.available_attacks = {
            'priest': ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK', 'strongLowerATK', 'rageSkill'],
            'thief': ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK', 'strongLowerATK'],
            'fighter': ['fastMiddleATK', 'fastLowerATK', 'fastUpperATK', 'strongMiddleATK', 'strongLowerATK', 'strongUpperATK']
        }

    def _load_font(self):
        """폰트 로드 시도"""
        try:
            # 프로젝트 루트의 폰트 파일 시도
            self.font = pico2d.load_font('ENCR10B.TTF', 16)
        except:
            try:
                # 기본 폰트 시도 (None을 전달하면 시스템 기본 폰트)
                self.font = pico2d.load_font(None, 16)
            except:
                # 폰트 로드 완전 실패
                self.font = None
                print("Warning: Font loading failed. HP text will not be displayed.")

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
        """현재 캐릭터의 이동속도 반환"""
        return self.character.get_move_speed()

    def initialize(self):
        self.character.initialize()  # Character 초기화
        # Character의 HP와 동기화
        self.character.hp = self.hp
        # 폰트 재로드 시도 (initialize 시점에서)
        if not self.font:
            self._load_font()

    def apply_gravity(self, deltaTime):
        """중력 적용"""
        if not self.is_grounded:
            # 중력으로 인한 Y방향 속도 증가
            self.velocity_y -= self.gravity * deltaTime
            # 위치 업데이트
            self.y += self.velocity_y * deltaTime

            # 그라운드 체크
            if self.y <= config.GROUND_Y:
                self.y = config.GROUND_Y
                self.velocity_y = 0.0
                self.is_grounded = True
        elif self.y > config.GROUND_Y:
            # 그라운드보다 높은 위치에 있으면 떨어지기 시작
            self.is_grounded = False
            self.velocity_y = 0.0

    def jump(self, jump_force=500.0):
        """점프 (필요시 사용)"""
        if self.is_grounded:
            self.velocity_y = jump_force
            self.is_grounded = False

    def check_collision_with_other_player(self, other_player):
        """다른 플레이어와의 충돌 검사"""
        if not other_player:
            return False

        my_bb = self.get_bb()
        other_bb = other_player.get_bb()

        # AABB 충돌 검사
        return (my_bb[0] < other_bb[2] and my_bb[2] > other_bb[0] and
                my_bb[1] < other_bb[3] and my_bb[3] > other_bb[1])

    def resolve_collision_with_other_player(self, other_player):
        """다른 플레이어와의 충돌 해결"""
        if not other_player:
            return

        if self.check_collision_with_other_player(other_player):
            # 충돌 시 이전 위치로 되돌리기
            self.x = self.prev_x

    def update_position(self, new_x, other_player=None):
        """위치 업데이트 (충돌 검사 포함)"""
        # 이전 위치 저장
        self.prev_x = self.x

        # 새 위치로 이동
        self.x = new_x

        # 화면 경계 체크
        screen_margin = 60  # 바운딩 박스 반폭 + 여유
        if self.x < screen_margin:
            self.x = screen_margin
        elif self.x > config.windowWidth - screen_margin:
            self.x = config.windowWidth - screen_margin

        # 다른 플레이어와의 충돌 체크 및 해결
        if other_player:
            self.resolve_collision_with_other_player(other_player)

    def start_guard(self):
        """가드 상태 시작"""
        self.is_guarding = True
        self.guard_timer = self.guard_duration
        self.state = 'guard'
        print(f"Player guarding! Position: {self.position_state}")

    def update_guard(self, deltaTime):
        """가드 상태 업데이트"""
        if self.is_guarding:
            self.guard_timer -= deltaTime
            if self.guard_timer <= 0:
                self.is_guarding = False
                if not self.is_attacking and not self.is_hit:
                    self.state = 'Idle'
                print("Guard ended")

    def can_guard_against_attack(self, attack_type):
        """공격 타입에 따른 가드 가능 여부 확인"""
        guard_mapping = {
            'fastUpperATK': 'High',
            'strongUpperATK': 'High',
            'fastMiddleATK': 'Middle',
            'strongMiddleATK': 'Middle',
            'fastLowerATK': 'Low',
            'strongLowerATK': 'Low'
        }

        required_position = guard_mapping.get(attack_type)
        if required_position and self.position_state == required_position:
            return True
        return False

    def get_attack_range_bb(self):
        """공격 범위의 바운딩 박스 반환 (PlayerLeft 기준)"""
        my_bb = self.get_bb()

        # fast 공격 범위: 바운딩 박스 오른쪽 끝에서 +20
        if 'fast' in self.state:
            attack_range = 20
            range_x1 = my_bb[2]  # 바운딩 박스 오른쪽 끝
            range_x2 = range_x1 + attack_range
            range_y1 = my_bb[1]
            range_y2 = my_bb[3]
            return range_x1, range_y1, range_x2, range_y2

        # strong 공격 범위는 필요에 따라 추가
        elif 'strong' in self.state:
            attack_range = 30  # strong 공격은 범위가 더 넓다고 가정
            range_x1 = my_bb[2]
            range_x2 = range_x1 + attack_range
            range_y1 = my_bb[1]
            range_y2 = my_bb[3]
            return range_x1, range_y1, range_x2, range_y2

        # rage 스킬 범위
        elif 'rage' in self.state:
            attack_range = 50  # rage 스킬은 범위가 가장 넓다고 가정
            range_x1 = my_bb[2]
            range_x2 = range_x1 + attack_range
            range_y1 = my_bb[1]
            range_y2 = my_bb[3]
            return range_x1, range_y1, range_x2, range_y2

        return None

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

    def can_hit_target(self):
        """타격 처리 가능 여부 확인 (한 공격당 한 번만)"""
        return self.is_attacking and not self.attack_hit_processed

    def mark_attack_hit_processed(self):
        """타격 처리 완료 마킹"""
        self.attack_hit_processed = True

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False, char_change_input=None, other_player=None, position_state='Middle'):
        # 위치 상태 업데이트
        self.position_state = position_state

        # 가드 상태 업데이트
        self.update_guard(deltaTime)

        # 캐릭터 타입 변경 처리 (공격 중이 아닐 때만)
        if char_change_input and not self.is_attacking and char_change_input in self.available_attacks:
            current_type = self.get_character_type()
            if current_type != char_change_input:
                self.set_character_type(char_change_input)
                return

        # 중력 적용 (항상)
        self.apply_gravity(deltaTime)

        # hit 상태 동기화
        self.is_hit = self.character.is_hit

        # 가드 중이면 다른 행동 불가
        if self.is_guarding:
            return

        # hit 상태일 때 기상 입력 처리
        if self.is_hit and self.character.can_get_up:
            # 아무 키 입력이 있으면 기상 시도
            if move_input or atk_input or combo_input:
                if self.character.try_get_up():
                    self.hit_recovery_input = True
                    return

        # hit 상태가 아닐 때만 일반 행동 처리
        if not self.is_hit:
            # 연계 공격 처리 (우선순위 1)
            if combo_input and self.can_combo and not self.combo_reserved:
                self.combo_reserved = True
                print(f"Combo reserved for {self.get_character_type()}")
                return

            # 새로운 공격 입력 처리 (공격 중이 아닐 때만)
            if not self.is_attacking and atk_input:
                # 캐릭터별 공격 제한 확인
                if self.can_use_attack(atk_input):
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

            # 공격 중이 아닐 때만 이동 처리
            if not self.is_attacking:
                move_speed = self.get_move_speed()
                if move_input == 'left':
                    new_x = self.x - move_speed * deltaTime
                    self.update_position(new_x, other_player)
                    self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
                elif move_input == 'right':
                    new_x = self.x + move_speed * deltaTime
                    self.update_position(new_x, other_player)
                    self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
                elif not move_input:
                    self.state = 'Idle'  # 입력이 없으면 Idle 상태

        # 캐릭터 위치 및 상태 동기화
        self.character.x, self.character.y = self.x, self.y
        if not self.is_hit and not self.is_guarding:  # hit 상태나 가드 상태가 아닐 때만 상태 동기화
            self.character.state = self.state
        self.character.hp = self.hp

        # Character 업데이트
        self.character.update(deltaTime)

    def take_damage(self, damage, attack_state='fastMiddleATK'):
        """데미지를 받는 메서드 - 공격 상태에 따른 hit 타입 결정"""
        # 공격 상태에 따른 hit 타입 결정
        attack_type = 'strong' if 'strong' in attack_state or 'rage' in attack_state else 'fast'

        # Character의 take_damage 호출
        self.character.take_damage(damage, attack_type)

        # Player HP 동기화
        self.hp = self.character.hp

        # 공격 상태 초기화 (피격 시 공격 중단)
        self.is_attacking = False
        self.can_combo = False
        self.combo_reserved = False

        return self.hp

    def is_in_hit_state(self):
        """현재 피격 상태인지 확인"""
        return self.is_hit

    def can_act(self):
        """행동 가능 상태인지 확인 (공격이나 이동 가능)"""
        return not self.is_attacking and not self.is_hit

    def get_bb(self):
        """바운딩 박스 좌표 반환 (x1, y1, x2, y2)"""
        # 바운딩 박스도 1.5배 스케일링
        bb_width = 40 * 1.5  # 60
        bb_height = 50 * 1.5  # 75
        return self.x - bb_width, self.y - bb_height, self.x + bb_width, self.y + bb_height

    def set_character_type(self, character_type):
        """캐릭터 타입 변경"""
        if character_type in self.available_attacks:
            self.character.set_character_type(character_type)
            # 공격 상태 초기화
            self.is_attacking = False
            self.can_combo = False
            self.combo_reserved = False
            self.state = 'Idle'

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

    def _render_hp_text(self):
        """HP 텍스트 렌더링"""
        if self.font:
            # HP 텍스트를 플레이어 위에 표시
            hp_text = f"HP: {self.hp}/{self.max_hp}"
            self.font.draw(self.x - 30, self.y + 80, hp_text, (255, 255, 255))

    def render(self):
        # 바운딩 박스 그리기
        pico2d.draw_rectangle(*self.get_bb())
        # HP 텍스트 렌더링
        self._render_hp_text()

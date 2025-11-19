from Character.character import Character
import pico2d
import pathlib


class Player:

    def __init__(self, x=600, y=450, character_type='priest'):  # 이미 스케일링된 위치
        self.x, self.y = x, y
        self.character = Character(character_type)  # Character 인스턴스 추가
        self.character.x, self.character.y = x, y  # 캐릭터 위치 동기화
        self.hp = 100  # HP 추가
        self.max_hp = 100  # 최대 HP

        self.dir = -1  # 항상 오른쪽을 바라보도록 -1로 고정
        self.state = 'Idle'  # Idle, Walk, BackWalk
        self.is_attacking = False  # 공격 중인지 체크
        self.can_combo = False  # 연계 가능 상태
        self.combo_reserved = False  # 연계 공격 예약 상태

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

    def update(self, deltaTime, move_input=None, atk_input=None, combo_input=False, char_change_input=None):
        # 캐릭터 타입 변경 처리 (공격 중이 아닐 때만)
        if char_change_input and not self.is_attacking and char_change_input in self.available_attacks:
            current_type = self.get_character_type()
            if current_type != char_change_input:
                self.set_character_type(char_change_input)
                return

        # 캐릭터 위치 및 HP 동기화
        self.character.x, self.character.y = self.x, self.y
        self.character.state = self.state
        self.character.hp = self.hp

        # Character 업데이트
        self.character.update(deltaTime)

        # 연계 공격 입력 처리
        if combo_input and self.can_combo:
            if (self.get_character_type() == 'priest' and self.state == 'strongMiddleATK') or \
               (self.get_character_type() == 'thief' and self.state in ['fastMiddleATK', 'fastMiddleATK2', 'strongMiddleATK', 'strongUpperATK']) or \
               (self.get_character_type() == 'fighter' and self.state in ['fastMiddleATK', 'fastMiddleATK2', 'strongUpperATK']):
                self.combo_reserved = True
                return

        # rage 스킬 입력 처리 (가장 높은 우선순위)
        if atk_input == 'rageSkill' and not self.is_attacking and self.can_use_attack('rageSkill'):
            self.state = 'rageSkill'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return

        # 공격 입력 처리 (이동 중에도 가능) - 캐릭터별 공격 제한 적용
        if atk_input == 'fastMiddleATK' and not self.is_attacking and self.can_use_attack('fastMiddleATK'):
            self.state = 'fastMiddleATK'
            self.is_attacking = True
            # thief와 fighter는 fastMiddleATK에서도 연계 가능
            self.can_combo = True if self.get_character_type() in ['thief', 'fighter'] else False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'fastLowerATK' and not self.is_attacking and self.can_use_attack('fastLowerATK'):
            self.state = 'fastLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'fastUpperATK' and not self.is_attacking and self.can_use_attack('fastUpperATK'):
            self.state = 'fastUpperATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongMiddleATK' and not self.is_attacking and self.can_use_attack('strongMiddleATK'):
            self.state = 'strongMiddleATK'
            self.is_attacking = True
            # 모든 캐릭터가 strongMiddleATK에서 연계 가능
            self.can_combo = True
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongUpperATK' and not self.is_attacking and self.can_use_attack('strongUpperATK'):
            self.state = 'strongUpperATK'
            self.is_attacking = True
            # thief와 fighter는 strongUpperATK에서도 연계 가능
            self.can_combo = True if self.get_character_type() in ['thief', 'fighter'] else False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시
        elif atk_input == 'strongLowerATK' and not self.is_attacking and self.can_use_attack('strongLowerATK'):
            self.state = 'strongLowerATK'
            self.is_attacking = True
            self.can_combo = False
            self.combo_reserved = False
            return  # 공격 시작 시 이동은 무시

        # 공격 중이 아닐 때만 이동 처리
        if not self.is_attacking:
            move_speed = self.get_move_speed()
            if move_input == 'left':
                self.x -= move_speed * deltaTime
                self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
            elif move_input == 'right':
                self.x += move_speed * deltaTime
                self.state = 'Walk'  # 기본은 Walk, 각 플레이어에서 오버라이드
            else:
                self.state = 'Idle'  # 입력이 없으면 Idle 상태

    def render(self):
        # SpriteManager에서 캐릭터 이미지를 렌더링하므로 여기서는 바운딩 박스와 HP만 그리기
        pico2d.draw_rectangle(*self.get_bb())  # 바운딩 박스 그리기

        # HP 텍스트 렌더링 (바운딩 박스 아래쪽)
        self._render_hp_text()

    def _render_hp_text(self):
        """HP 텍스트 렌더링 메서드"""
        if not self.font:
            return

        bb_x1, bb_y1, bb_x2, bb_y2 = self.get_bb()
        text_x = (bb_x1 + bb_x2) // 2  # 바운딩 박스 중앙
        text_y = bb_y1 - 30  # 바운딩 박스 아래 30픽셀

        # HP 텍스트 색상 결정
        hp_percentage = self.hp / self.max_hp
        if hp_percentage > 0.6:
            text_color = (0, 255, 0)  # 초록색
        elif hp_percentage > 0.3:
            text_color = (255, 255, 0)  # 노란색
        else:
            text_color = (255, 0, 0)  # 빨간색

        # HP 텍스트 출력
        try:
            self.font.draw(text_x - 15, text_y, f"HP: {self.hp}", text_color)
        except:
            # 폰트 오류 시 무시
            pass

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

    def take_damage(self, damage):
        """데미지를 받는 메서드"""
        self.hp = max(0, self.hp - damage)
        self.character.hp = self.hp
        return self.hp

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

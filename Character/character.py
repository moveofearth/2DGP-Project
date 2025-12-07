import pico2d
import pathlib
import config


class Character:
    def __init__(self, character_type='priest'):
        self.currentCharacter = character_type  # 현재 캐릭터 타입
        self.image = None
        self.frame = 0
        self.x, self.y = 400, config.GROUND_Y  # 그라운드에 위치
        self.state = 'Idle'
        self.hp = 100  # HP 추가
        self.max_hp = 100  # 최대 HP 추가

        # hit 상태 관련 속성 추가
        self.is_hit = False
        self.hit_type = None  # 'fast' 또는 'strong'
        self.hit_frame_range = (0, 1)  # hit 프레임 범위
        self.hit_frame_start = 0  # hit 시작 프레임
        self.can_get_up = False  # 기상 가능 상태

        # 물리 변수 추가
        self.velocity_y = 0.0
        self.is_grounded = True

        # 캐릭터별 이동속도 설정 (70% 증가)
        self.move_speeds = {
            'priest': 306.0,  # 180 * 1.7
            'thief': 374.0,   # 220 * 1.7
            'fighter': 340.0  # 200 * 1.7
        }

    def initialize(self):
        # 캐릭터 타입에 따른 초기화
        if self.currentCharacter in ['priest', 'thief', 'fighter']:
            self._initialize_character()

    def _initialize_character(self):
        """모든 캐릭터 공통 초기화"""
        # 캐릭터 전용 초기화 로직
        pass

    def update(self, deltaTime):
        # 캐릭터 타입에 따른 업데이트
        if self.currentCharacter in ['priest', 'thief', 'fighter']:
            self._update_character(deltaTime)

    def render(self):
        if self.image:  # 이미지 None 체크 추가
            self.image.draw(self.x, self.y)

    def set_character_type(self, character_type):
        """캐릭터 타입 변경"""
        if character_type in ['priest', 'thief', 'fighter']:
            self.currentCharacter = character_type
            self.initialize()  # 새 캐릭터로 초기화

    def get_character_type(self):
        """현재 캐릭터 타입 반환"""
        return self.currentCharacter

    def get_move_speed(self):
        """현재 캐릭터의 이동속도 반환"""
        return self.move_speeds.get(self.currentCharacter, 150.0)  # 기본값도 낮춤

    def take_damage(self, damage, attack_type='fast'):
        """데미지를 받는 메서드 - airborne 타입 추가"""
        self.hp = max(0, self.hp - damage)

        # hit 상태 설정
        self.is_hit = True
        self.hit_type = attack_type
        self.state = 'hit'

        # 공격 타입에 따른 hit 프레임 범위 설정
        if attack_type == 'fast':
            self.hit_frame_range = (0, 1)
            self.can_get_up = False
        elif attack_type == 'strong':
            self.hit_frame_range = (0, 4)
            self.can_get_up = True
        elif attack_type == 'airborne':
            # 공중에 뜨는 상태 - 프레임은 공중에서 계속 0번 유지
            self.hit_frame_range = (0, 0)
            self.can_get_up = False  # 공중에서는 기상 불가
        elif attack_type == 'down':
            # down 상태 (땅에 누운 상태)
            self.hit_frame_range = (4, 4)
            self.can_get_up = True

        self.hit_frame_start = self.hit_frame_range[0]
        self.frame = self.hit_frame_start

        print(f"Character hit! Type: {attack_type}, HP: {self.hp}, frame: {self.frame}")
        return self.hp

    def try_get_up(self):
        """기상 시도 - down/strong 상태에서 SpriteManager가 허용한 경우 기상 처리"""
        # SpriteManager가 프레임 도달 시 can_get_up=True로 설정하므로,
        # 여기서는 그 플래그만으로 기상을 허용하도록 변경.
        if self.can_get_up and self.is_hit:
            if self.hit_type in ('strong', 'down'):
                # 즉시 기상 프레임으로 전환하고 기상 플래그 제거
                self.frame = 5
                self.can_get_up = False
                print(f"Character getting up from {self.hit_type} state -> frame {self.frame}")
                return True
        return False

    def reset_hit_state(self):
        """hit 상태 초기화"""
        self.is_hit = False
        self.hit_type = None
        self.can_get_up = False
        self.frame = 0
        if self.state == 'hit':
            self.state = 'Idle'
        print("Character hit state reset")

    def _update_character(self, deltaTime):
        """모든 캐릭터 공통 업데이트"""
        # hit 상태에서 자동 회복 로직 (fast 공격의 경우)
        if self.is_hit and self.hit_type == 'fast':
            # fast 공격은 짧은 시간 후 자동으로 회복
            pass  # SpriteManager에서 처리

        # 캐릭터 전용 업데이트 로직
        pass

    def heal(self, amount):
        """체력을 회복하는 메서드"""
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp

    def is_alive(self):
        """생존 여부 확인"""
        return self.hp > 0

    def get_hp_percentage(self):
        """HP 퍼센테이지 반환 (0.0 ~ 1.0)"""
        return self.hp / self.max_hp if self.max_hp > 0 else 0.0

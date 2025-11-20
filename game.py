import pico2d
import config
import time

from Scenes.sceneManager import SceneManager
from Player.playerLeft import PlayerLeft
from Player.playerRight import PlayerRight
from ioManager import IOManager
from spriteManager import SpriteManager


class Game:

    def __init__(self):
        self.running = True
        self.sceneManager = SceneManager()
        self.playerLeft = PlayerLeft()
        self.playerRight = PlayerRight()
        self.ioManager = IOManager()
        self.spriteManager = SpriteManager()
        self.last_time = 0
        self.target_fps = 60  # 60fps로 조정
        self.frame_time = 1.0 / self.target_fps
        self.game_over = False
        self.max_delta_time = 1.0 / 30.0  # 최대 deltaTime 제한 (30fps 이하로 떨어지지 않도록)

    def initialize(self):
        pico2d.open_canvas(config.windowWidth, config.windowHeight)
        self.sceneManager.initialize()
        self.playerLeft.initialize()
        self.playerRight.initialize()
        self.spriteManager.load_sprites()
        self.spriteManager.set_player_references(self.playerLeft, self.playerRight)
        self.last_time = time.time()

    def check_collision(self):
        """플레이어 간 충돌 및 공격 판정 - 공격 범위 기반"""
        # Player1이 공격 중이고 타격 처리 가능한 상태인지 확인
        if (self.playerLeft.is_attacking and
            hasattr(self.playerLeft, 'can_process_hit') and
            self.playerLeft.can_process_hit and
            self.playerLeft.can_hit_target()):

            # PlayerRight가 down 상태일 때 Lower 계열 공격은 히트 가능하도록 허용
            attacker_state = self.playerLeft.state or ''
            target = self.playerRight
            # 대상의 현재 hit_type 확인 (down 또는 airborne일 때 특별 처리 허용)
            target_hit_type = getattr(target.character, 'hit_type', None) if hasattr(target, 'character') else None
            target_is_down = (target_hit_type == 'down')
            target_is_airborne = (target_hit_type == 'airborne')
            # lower 계열 공격은 down 상태에 대한 히트 허용, 그리고 공중(airborne) 상태도 추가 허용
            allow_hit_on_down = ('lower' in attacker_state.lower()) and target_is_down
            allow_hit_on_airborne = target_is_airborne

            # 기본적으로는 피격 상태가 아니어야 히트되지만,
            # down(낙하 후) 또는 airborne(공중) 상태인 경우엔 추가 히트 허용
            if (not target.is_in_hit_state()) or allow_hit_on_down or allow_hit_on_airborne:

                # Player1의 공격 범위에 Player2가 있는지 확인
                if self.playerLeft.is_in_attack_range(self.playerRight):
                    # 가드 판정 먼저 확인
                    if self.playerRight.can_guard_against_attack(self.playerLeft.state):
                        # 가드 성공 - 데미지 없음, 가드 지속 또는 시작
                        self.playerRight.start_guard()
                        print(f"Player2 successfully guarded against {self.playerLeft.state}! Position: {self.playerRight.position_state}")
                    else:
                        # 가드 실패 - 데미지 적용
                        damage = self.calculate_damage(self.playerLeft.state)
                        # 공격자 참조 전달 (포물선 방향 계산용)
                        self.playerRight.take_damage(damage, self.playerLeft.state, attacker=self.playerLeft)
                        print(f"Player2 took {damage} damage! HP: {self.playerRight.get_hp()}, State: hit")

                    # 타격 처리 완료 마킹
                    self.playerLeft.mark_attack_hit_processed()
                    self.playerLeft.can_process_hit = False

        # Player2가 공격 중이고 타격 처리 가능한 상태인지 확인
        if (self.playerRight.is_attacking and
            hasattr(self.playerRight, 'can_process_hit') and
            self.playerRight.can_process_hit and
            self.playerRight.can_hit_target()):

            # PlayerLeft가 down 상태일 때 Lower 계열 공격은 히트 가능하도록 허용
            attacker_state = self.playerRight.state or ''
            target = self.playerLeft
            target_hit_type = getattr(target.character, 'hit_type', None) if hasattr(target, 'character') else None
            target_is_down = (target_hit_type == 'down')
            target_is_airborne = (target_hit_type == 'airborne')
            allow_hit_on_down = ('lower' in attacker_state.lower()) and target_is_down
            allow_hit_on_airborne = target_is_airborne

            if (not target.is_in_hit_state()) or allow_hit_on_down or allow_hit_on_airborne:

                # Player2의 공격 범위에 Player1이 있는지 확인
                if self.playerRight.is_in_attack_range(self.playerLeft):
                    # 가드 판정 먼저 확인
                    if self.playerLeft.can_guard_against_attack(self.playerRight.state):
                        # 가드 성공 - 데미지 없음, 가드 지속 또는 시작
                        self.playerLeft.start_guard()
                        print(f"Player1 successfully guarded against {self.playerRight.state}! Position: {self.playerLeft.position_state}")
                    else:
                        # 가드 실패 - 데미지 적용
                        damage = self.calculate_damage(self.playerRight.state)
                        # 공격자 참조 전달 (포물선 방향 계산용)
                        self.playerLeft.take_damage(damage, self.playerRight.state, attacker=self.playerRight)
                        print(f"Player1 took {damage} damage! HP: {self.playerLeft.get_hp()}, State: hit")

                    # 타격 처리 완료 마킹
                    self.playerRight.mark_attack_hit_processed()
                    self.playerRight.can_process_hit = False

    def calculate_damage(self, attack_state):
        """공격 상태에 따른 데미지 계산"""
        # fast 공격들은 모두 10데미지
        if 'fast' in attack_state.lower():
            return 10
        # strong 공격들은 모두 20데미지
        elif 'strong' in attack_state.lower():
            return 20
        # rage 스킬은 특별히 30데미지
        elif 'rage' in attack_state.lower():
            return 30
        else:
            # 기본 데미지 (혹시 모를 다른 공격들)
            return 5

    def update(self, deltaTime):
        # deltaTime 제한 - 너무 큰 값이 들어오면 제한
        deltaTime = min(deltaTime, self.max_delta_time)

        events = pico2d.get_events()

        # ESC 키로 종료 처리
        if self.ioManager.checkEscape(events):
            self.running = False
            return

        # 종료 이벤트 처리
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                self.running = False

        # 타이틀 씬에서는 스페이스바만 처리
        if self.sceneManager.is_title_scene():
            if self.ioManager.handleSpaceInput(events):
                self.sceneManager.change_to_play_scene()
            return

        # 게임 오버 상태면 업데이트 중지
        if self.game_over:
            return

        # 플레이어 입력 처리
        player1_move_input = self.ioManager.handleMoveInputPlayer1(events)
        player1_atk_input = self.ioManager.handleATKInputPlayer1(events)
        player1_char_change = self.ioManager.handleCharacterChangePlayer1(events)
        player1_position_state = self.ioManager.get_player1_position_state()
        player1_getup_input = self.ioManager.check_player1_getup_input()  # 기상 입력 추가

        player2_move_input = self.ioManager.handleMoveInputPlayer2(events)
        player2_atk_input = self.ioManager.handleATKInputPlayer2(events)
        player2_position_state = self.ioManager.get_player2_position_state()
        player2_getup_input = self.ioManager.check_player2_getup_input()  # 기상 입력 추가

        # 연계 입력 확인
        player1_combo = self.ioManager.check_player1_combo_input()
        player2_combo = self.ioManager.check_player2_combo_input()

        # 플레이어 업데이트 (기상 입력 포함)
        self.playerLeft.update(deltaTime, player1_move_input, player1_atk_input, player1_combo, player1_char_change, self.playerRight, player1_position_state, player1_getup_input)
        self.playerRight.update(deltaTime, player2_move_input, player2_atk_input, player2_combo, None, self.playerLeft, player2_position_state, player2_getup_input)

        # 충돌 및 공격 판정
        self.check_collision()

        # 게임 오버 체크
        if not self.playerLeft.is_alive() or not self.playerRight.is_alive():
            self.game_over = True
            winner = "Player2" if not self.playerLeft.is_alive() else "Player1"
            print(f"Game Over! {winner} wins!")

        # SpriteManager에 플레이어 상태 전달 - 플레이어 업데이트 후에 실행
        self.spriteManager.update_player1_state(self.playerLeft.state, deltaTime)
        self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
        self.spriteManager.update_player1_direction(self.playerLeft.dir)

        self.spriteManager.update_player2_state(self.playerRight.state, deltaTime)
        self.spriteManager.update_player2_position(self.playerRight.x, self.playerRight.y)
        self.spriteManager.update_player2_direction(self.playerRight.dir)

    def render(self):
        pico2d.clear_canvas()
        self.sceneManager.render()

        # 플레이 씬에서만 플레이어 렌더링
        if not self.sceneManager.is_title_scene():
            self.spriteManager.render()
            # 바운딩 박스 및 HP 렌더링을 위해 플레이어 render 호출
            self.playerLeft.render()
            self.playerRight.render()

            # 게임 오버 메시지 렌더링
            if self.game_over:
                # 간단한 게임 오버 표시 (폰트가 있는 경우)
                if hasattr(self.playerLeft, 'font') and self.playerLeft.font:
                    winner = "Player2" if self.playerLeft.is_alive() else "Player1"
                    self.playerLeft.font.draw(960, 540, f"Game Over! {winner} wins!", (255, 255, 255))

        pico2d.update_canvas()

    def run(self):
        current_time = time.time()
        deltaTime = current_time - self.last_time

        # 첫 프레임에서 deltaTime이 너무 크지 않도록 제한
        if self.last_time == 0:
            deltaTime = self.frame_time

        # 프레임 제한 - 너무 빠르면 대기
        if deltaTime < self.frame_time:
            time.sleep(self.frame_time - deltaTime)
            current_time = time.time()
            deltaTime = current_time - self.last_time

        self.last_time = current_time

        self.update(deltaTime)
        self.render()

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
        self.target_fps = 70
        self.frame_time = 1.0 / self.target_fps
        self.game_over = False

    def initialize(self):
        pico2d.open_canvas(config.windowWidth, config.windowHeight)
        self.sceneManager.initialize()
        self.playerLeft.initialize()
        self.playerRight.initialize()
        self.spriteManager.load_sprites()
        self.spriteManager.set_player_references(self.playerLeft, self.playerRight)
        self.last_time = time.time()

    def check_collision(self):
        """플레이어 간 충돌 및 공격 판정"""
        # 두 플레이어의 바운딩 박스 가져오기
        p1_bb = self.playerLeft.get_bb()
        p2_bb = self.playerRight.get_bb()

        # 바운딩 박스 충돌 검사 (공격 판정용)
        if (p1_bb[0] < p2_bb[2] and p1_bb[2] > p2_bb[0] and
            p1_bb[1] < p2_bb[3] and p1_bb[3] > p2_bb[1]):

            # 공격 중인 플레이어가 있는지 확인
            if self.playerLeft.is_attacking and not self.playerRight.is_attacking:
                # Player1이 공격 중이면 Player2가 데미지 받음
                damage = self.calculate_damage(self.playerLeft.state)
                self.playerRight.take_damage(damage)
                print(f"Player2 took {damage} damage! HP: {self.playerRight.get_hp()}")

            elif self.playerRight.is_attacking and not self.playerLeft.is_attacking:
                # Player2가 공격 중이면 Player1이 데미지 받음
                damage = self.calculate_damage(self.playerRight.state)
                self.playerLeft.take_damage(damage)
                print(f"Player1 took {damage} damage! HP: {self.playerLeft.get_hp()}")

    def calculate_damage(self, attack_state):
        """공격 상태에 따른 데미지 계산"""
        damage_table = {
            'fastMiddleATK': 5,
            'fastLowerATK': 5,
            'fastUpperATK': 5,
            'strongMiddleATK': 10,
            'strongUpperATK': 12,
            'strongLowerATK': 10,
            'rageSkill': 20
        }
        return damage_table.get(attack_state, 3)

    def update(self, deltaTime):
        events = pico2d.get_events()

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

        # 플레이 씬에서만 플레이어 입력 처리
        # 이동과 공격 입력을 분리해서 처리
        player1_move_input = self.ioManager.handleMoveInputPlayer1(events)
        player1_atk_input = self.ioManager.handleATKInputPlayer1(events)
        player1_char_change = self.ioManager.handleCharacterChangePlayer1(events)
        player1_position_state = self.ioManager.get_player1_position_state()

        player2_move_input = self.ioManager.handleMoveInputPlayer2(events)
        player2_atk_input = self.ioManager.handleATKInputPlayer2(events)
        player2_position_state = self.ioManager.get_player2_position_state()

        # 연계 입력 확인
        player1_combo = self.ioManager.check_player1_combo_input()
        player2_combo = self.ioManager.check_player2_combo_input()

        # 플레이어 업데이트 시 서로의 참조를 전달하여 충돌 처리
        self.playerLeft.update(deltaTime, player1_move_input, player1_atk_input, player1_combo, player1_char_change, self.playerRight, player1_position_state)
        self.playerRight.update(deltaTime, player2_move_input, player2_atk_input, player2_combo, None, self.playerLeft, player2_position_state)

        # 충돌 및 공격 판정
        self.check_collision()

        # 게임 오버 체크
        if not self.playerLeft.is_alive() or not self.playerRight.is_alive():
            self.game_over = True
            winner = "Player2" if self.playerLeft.is_alive() else "Player1"
            print(f"Game Over! {winner} wins!")

        # SpriteManager에 플레이어 상태 전달
        self.spriteManager.update_player1_state(self.playerLeft.state, deltaTime)
        self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
        self.spriteManager.update_player1_direction(self.playerLeft.dir)

        # 플레이어2 상태 전달
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

        # 프레임 제한 - 너무 빠르면 대기
        if deltaTime < self.frame_time:
            time.sleep(self.frame_time - deltaTime)
            current_time = time.time()
            deltaTime = current_time - self.last_time

        self.last_time = current_time

        self.update(deltaTime)
        self.render()

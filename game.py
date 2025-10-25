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

    def initialize(self):
        pico2d.open_canvas(Config.windowWidth, Config.windowHeight)
        self.sceneManager.initialize()
        self.playerLeft.initialize()
        self.playerRight.initialize()
        self.spriteManager.load_sprites()
        self.spriteManager.set_player_references(self.playerLeft, self.playerRight)
        self.last_time = time.time()

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

        # 플레이 씬에서만 플레이어 입력 처리
        # 이동과 공격 입력을 분리해서 처리
        player1_move_input = self.ioManager.handleMoveInputPlayer1(events)
        player1_atk_input = self.ioManager.handleATKInputPlayer1(events)
        player1_char_change = self.ioManager.handleCharacterChangePlayer1(events)
        player2_move_input = self.ioManager.handleMoveInputPlayer2(events)
        player2_atk_input = self.ioManager.handleATKInputPlayer2(events)

        # 연계 입력 확인
        player1_combo = self.ioManager.check_player1_combo_input()
        player2_combo = self.ioManager.check_player2_combo_input()

        # 플레이어 업데이트 시 이동, 공격, 연계, 캐릭터 변경 입력을 모두 전달
        self.playerLeft.update(deltaTime, player1_move_input, player1_atk_input, player1_combo, player1_char_change)
        self.playerRight.update(deltaTime, player2_move_input, player2_atk_input, player2_combo)

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

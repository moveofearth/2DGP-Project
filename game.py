import pico2d
import Config

from Scenes.sceneManager import SceneManager
from Player.playerLeft import PlayerLeft
from Player.playerRight import PlayerRight  # PlayerRight 추가
from ioManager import IOManager
from spriteManager import SpriteManager


class Game:

    def __init__(self):
        self.running = True
        self.sceneManager = SceneManager()
        self.playerLeft = PlayerLeft()
        self.playerRight = PlayerRight()  # PlayerRight 추가
        self.ioManager = IOManager()
        self.spriteManager = SpriteManager()
        pass

    def initialize(self):
        pico2d.open_canvas(Config.windowWidth, Config.windowHeight)
        self.sceneManager.initialize()
        self.playerLeft.initialize()
        self.playerRight.initialize()  # PlayerRight 초기화
        self.spriteManager.load_sprites()
        self.spriteManager.set_player_references(self.playerLeft, self.playerRight)  # 플레이어 참조 설정
        pass

    def update(self, deltaTime):
        events = pico2d.get_events()

        # 이동과 공격 입력을 분리해서 처리
        player1_move_input = self.ioManager.handleMoveInputPlayer1(events)
        player1_atk_input = self.ioManager.handleATKInputPlayer1(events)
        player2_move_input = self.ioManager.handleMoveInputPlayer2(events)
        player2_atk_input = self.ioManager.handleATKInputPlayer2(events)

        # 연계 입력 확인
        player1_combo = self.ioManager.check_player1_combo_input()
        player2_combo = self.ioManager.check_player2_combo_input()

        # 플레이어 업데이트 시 이동, 공격, 연계 입력을 모두 전달
        self.playerLeft.update(deltaTime, player1_move_input, player1_atk_input, player1_combo)
        self.playerRight.update(deltaTime, player2_move_input, player2_atk_input, player2_combo)

        # SpriteManager에 플레이어 상태 전달
        self.spriteManager.update_player1_state(self.playerLeft.state, deltaTime)
        self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
        self.spriteManager.update_player1_direction(self.playerLeft.dir)

        # 플레이어2 상태 전달
        self.spriteManager.update_player2_state(self.playerRight.state, deltaTime)
        self.spriteManager.update_player2_position(self.playerRight.x, self.playerRight.y)
        self.spriteManager.update_player2_direction(self.playerRight.dir)
        pass

    def render(self):
        pico2d.clear_canvas()
        self.sceneManager.render()
        self.spriteManager.render()
        pico2d.update_canvas()
        pass

    def run(self):
        self.update(deltaTime=0.01)
        self.render()
        pass
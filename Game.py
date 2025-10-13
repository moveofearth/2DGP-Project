import pico2d
import Config

from scenes.SceneManager import SceneManager
from player.PlayerLeft import PlayerLeft
from player.PlayerRight import PlayerRight  # PlayerRight 추가
from IOManager import IOManager
from SpriteManager import SpriteManager


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
        pass

    def update(self, deltaTime):
        events = pico2d.get_events()
        player1_input = self.ioManager.handleInputPlayer1(events)
        player2_input = self.ioManager.handleInputPlayer2(events)  # 플레이어2 입력 처리

        self.playerLeft.update(deltaTime, player1_input)
        self.playerRight.update(deltaTime, player2_input)  # 플레이어2 업데이트

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
        pico2d.delay(0.01)
        pass
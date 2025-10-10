import pico2d
import Config

from scenes.SceneManager import SceneManager  # import 수정
from player.PlayerLeft import PlayerLeft  # import 수정
from IOManager import IOManager  # IOManager 연결 추가


class Game:

    def __init__(self):
        self.running = True
        self.sceneManager = SceneManager()
        self.playerLeft = PlayerLeft()
        self.ioManager = IOManager()  # IOManager 초기화 추가
        pass

    def initialize(self):
        pico2d.open_canvas(Config.windowWidth, Config.windowHeight)
        self.sceneManager.initialize()
        self.playerLeft.initialize()
        pass

    def update(self, deltaTime):
        events = pico2d.get_events()  # 프레임마다 이벤트 가져오기 (IOManager에서 이동)
        player1_input = self.ioManager.handleInputPlayer1(events)  # 이벤트 전달
        self.playerLeft.update(deltaTime, player1_input)  # 입력을 Player에 연결
        pass

    def render(self):
        pico2d.clear_canvas()
        self.sceneManager.render()
        self.playerLeft.render()
        pico2d.update_canvas()
        pass

    def run(self):
        self.update(deltaTime=0.05)  # deltaTime 조정 (delay와 맞춤)
        self.render()
        pico2d.delay(0.05)
        pass
import pico2d
import Config

from scenes.SceneManager import SceneManager  # import 수정
from player.PlayerLeft import PlayerLeft  # import 수정
from IOManager import IOManager  # IOManager 연결 추가
from SpriteManager import SpriteManager  # SpriteManager 추가


class Game:

    def __init__(self):
        self.running = True
        self.sceneManager = SceneManager()
        self.playerLeft = PlayerLeft()
        self.ioManager = IOManager()  # IOManager 초기화 추가
        self.spriteManager = SpriteManager()  # SpriteManager 추가
        pass

    def initialize(self):
        pico2d.open_canvas(Config.windowWidth, Config.windowHeight)
        self.sceneManager.initialize()
        self.playerLeft.initialize()
        self.spriteManager.load_sprites()  # 스프라이트 로드
        pass

    def update(self, deltaTime):
        events = pico2d.get_events()  # 프레임마다 이벤트 가져오기 (IOManager에서 이동)
        player1_input = self.ioManager.handleInputPlayer1(events)  # 이벤트 전달
        self.playerLeft.update(deltaTime, player1_input)  # 입력을 Player에 연결

        # SpriteManager에 플레이어 상태 전달
        self.spriteManager.update_player1_state(self.playerLeft.state, deltaTime)
        self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
        self.spriteManager.update_player1_direction(self.playerLeft.dir)
        pass

    def render(self):
        pico2d.clear_canvas()
        self.sceneManager.render()
        # self.playerLeft.render()  # 기존 플레이어 렌더링 대신 SpriteManager 사용
        self.spriteManager.render()  # SpriteManager로 렌더링
        pico2d.update_canvas()
        pass

    def run(self):
        self.update(deltaTime=0.01)  # deltaTime 조정 (delay와 맞춤)
        self.render()
        pico2d.delay(0.01)
        pass
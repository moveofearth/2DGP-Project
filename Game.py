import pico2d
import Config
import SceneManager


class Game:
    def __init__(self):
        self.running = True
        self.sceneManager = SceneManager.SceneManager()
        pass

    def initialize(self):
        pico2d.open_canvas(Config.windowWidth, Config.windowHeight)
        self.sceneManager.initialize()
        #TODO / Initialize Managers
        pass

    def update(self, deltaTime):
        #TODO / Update Managers
        pass

    def render(self):
        pico2d.clear_canvas()
        self.sceneManager.render()
        pico2d.update_canvas()
        pico2d.delay(0.05)
        #TODO / Render Managers
        pass

    def run(self):
        self.update(deltaTime=0.1)
        self.render()
        pass
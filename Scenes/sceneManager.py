from Scenes.titleScene import TitleScene  # import 수정: 패키지.모듈 import 클래스


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.currentScene = None

    def addScene(self, sceneName, scene):
        self.scenes[sceneName] = scene

    def initialize(self):
        self.addScene("Title", TitleScene())  # 인스턴스 생성 수정
        self.changeScene("Title")

    def changeScene(self, sceneName):
        self.currentScene = self.scenes[sceneName]
        self.currentScene.initialize()

    def render(self):
        if self.currentScene is not None:
            self.currentScene.render()

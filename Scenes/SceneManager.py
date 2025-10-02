from Scenes import TitleScene


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.currentScene = None
        pass

    def addScene(self, sceneName, scene):
        self.scenes[sceneName] = scene
        pass

    def initialize(self):
        self.addScene("Title", TitleScene.TitleScene())
        self.changeScene("Title")
        pass


    def changeScene(self, sceneName):
        self.currentScene = self.scenes[sceneName]
        self.currentScene.initialize()
        pass

    def render(self):
        if self.currentScene is not None:
            self.currentScene.render()
        pass




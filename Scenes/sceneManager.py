import pico2d
from Scenes import titleScene
from Scenes import playScene
from Scenes import characterSelectScene


class SceneManager:
    def __init__(self):
        self.current_scene = 'title'  # 'title', 'character_select', 'play'
        self.title_scene = titleScene.TitleScene()
        self.character_select_scene = characterSelectScene.CharacterSelectScene()
        self.play_scene = playScene.PlayScene()

    def initialize(self):
        self.title_scene.initialize()
        self.character_select_scene.initialize()
        self.play_scene.initialize()

    def change_to_character_select(self):
        """캐릭터 선택 씬으로 전환"""
        self.character_select_scene.reset()  # 씬 리셋
        self.current_scene = 'character_select'

    def change_to_play_scene(self):
        """플레이 씬으로 전환"""
        self.current_scene = 'play'

    def is_title_scene(self):
        """현재 타이틀 씬인지 확인"""
        return self.current_scene == 'title'

    def is_character_select_scene(self):
        """현재 캐릭터 선택 씬인지 확인"""
        return self.current_scene == 'character_select'

    def update(self, deltaTime):
        if self.current_scene == 'title':
            self.title_scene.update(deltaTime)
        elif self.current_scene == 'character_select':
            self.character_select_scene.update(deltaTime)
        elif self.current_scene == 'play':
            self.play_scene.update(deltaTime)

    def render(self):
        pico2d.clear_canvas()
        if self.current_scene == 'title':
            self.title_scene.render()
        elif self.current_scene == 'character_select':
            self.character_select_scene.render()
        elif self.current_scene == 'play':
            self.play_scene.render()

    def get_character_select_scene(self):
        """캐릭터 선택 씬 반환"""
        return self.character_select_scene

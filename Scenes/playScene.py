import pico2d
import pathlib

class PlayScene:
    def __init__(self):
        self.background = None
        self.hp_ui = None

    def initialize(self):
        # 플레이 배경 이미지 로딩
        base_path = pathlib.Path.cwd() / 'Resources' / 'Scene'
        self.background = pico2d.load_image(str(base_path / 'stage.png'))

        # HP UI 이미지 로딩
        ui_path = pathlib.Path.cwd() / 'Resources' / 'UI'
        self.hp_ui = pico2d.load_image(str(ui_path / 'hp.png'))

    def update(self, deltaTime):
        pass

    def render(self):
        if self.background:
            self.background.draw(640, 360)  # 화면 중앙에 그리기

        # HP UI 렌더링
        if self.hp_ui:
            # 좌상단 HP (플레이어1용) - 중앙에 더 가깝게
            self.hp_ui.draw(320, 650)  # 좌측에서 중앙 쪽으로 이동

            # 우상단 HP (플레이어2용) - 좌우 반전, 중앙에 더 가깝게
            hp_width = self.hp_ui.w
            hp_height = self.hp_ui.h
            self.hp_ui.clip_composite_draw(
                0, 0, hp_width, hp_height,  # 전체 이미지 클립
                0, 'h',  # 좌우 반전
                960, 650,  # 우측에서 중앙 쪽으로 이동
                hp_width, hp_height  # 원본 크기
            )

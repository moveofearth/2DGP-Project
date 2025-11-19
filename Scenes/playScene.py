import pico2d
import pathlib

class PlayScene:
    def __init__(self):
        self.background = None
        self.hp_ui = None
        self.count_ui = None

    def initialize(self):
        # 플레이 배경 이미지 로딩
        base_path = pathlib.Path.cwd() / 'Resources' / 'Scene'
        self.background = pico2d.load_image(str(base_path / 'stage.png'))

        # HP UI 이미지 로딩
        ui_path = pathlib.Path.cwd() / 'Resources' / 'UI'
        self.hp_ui = pico2d.load_image(str(ui_path / 'hp.png'))
        self.count_ui = pico2d.load_image(str(ui_path / 'count.png'))

    def update(self, deltaTime):
        pass

    def render(self):
        if self.background:
            # 배경을 2배 스케일링하여 전체 화면에 맞춤 (960x540 -> 1920x1080)
            self.background.draw(960, 540, self.background.w * 2, self.background.h * 2)

        # HP UI 렌더링 - 1.5배 스케일링 및 위치 조정
        if self.hp_ui:
            scaled_width = self.hp_ui.w * 1.5
            scaled_height = self.hp_ui.h * 1.5

            # 좌상단 HP (플레이어1용) - 기존 320 위치를 1.5배로 스케일링
            self.hp_ui.draw(480, 980, scaled_width, scaled_height)

            # 우상단 HP (플레이어2용) - 좌우 반전, 기존 960 위치를 1.5배로 스케일링
            self.hp_ui.clip_composite_draw(
                0, 0, self.hp_ui.w, self.hp_ui.h,  # 전체 이미지 클립
                0, 'h',  # 좌우 반전
                1440, 980,  # 우측 위치 (960 * 1.5 = 1440)
                scaled_width, scaled_height
            )

        # Count UI 렌더링 - 1.5배 스케일링 및 위치 조정
        if self.count_ui:
            scaled_count_width = self.count_ui.w * 1.5
            scaled_count_height = self.count_ui.h * 1.5

            # 왼쪽 플레이어용 - 3개 가로 배치 (기존 220 위치를 1.5배로 스케일링)
            for i in range(3):
                self.count_ui.draw(330 + i * (scaled_count_width + 15), 870,
                                 scaled_count_width, scaled_count_height)

            # 오른쪽 플레이어용 - 3개 가로 배치 (좌우 반전)
            for i in range(3):
                self.count_ui.clip_composite_draw(
                    0, 0, self.count_ui.w, self.count_ui.h,
                    0, 'h',  # 좌우 반전
                    1290 + i * (scaled_count_width + 15), 870,
                    scaled_count_width, scaled_count_height
                )

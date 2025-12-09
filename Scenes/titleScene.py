import pico2d
import config  # 기존 그대로
import pathlib

class TitleScene:
    def __init__(self):
        self.image = None
        self.font = None
        self.bgm = None
    def initialize(self):
        path = pathlib.Path.cwd() / 'Resources' / 'Scene' / 'title.png'
        self.image = pico2d.load_image(str(path))
        self.font = pico2d.load_font('ENCR10B.TTF', 48)
        self.bgm = pico2d.load_music(str(pathlib.Path.cwd() / 'Resources' / 'Sound' / 'titleMusic.mp3'))
        self.bgm.set_volume(8)
        self.bgm.repeat_play()

    def update(self, deltaTime):
        pass
    def render(self):
        if self.image:
            # 화면 크기에 맞게 스트레치
            self.image.draw(config.windowWidth // 2, config.windowHeight // 2,
                          config.windowWidth, config.windowHeight)
        if self.font:
            # 화면 중간 하단부에 텍스트 표시
            self.font.draw(config.windowWidth // 2 - 250, config.windowHeight // 5 - 100,
                          'PRESS SPACE TO START', (0, 0, 0))

    def render_with_offset(self, offset_x):
        """오프셋을 적용하여 렌더링 (슬라이드 효과용)"""
        if self.image:
            # 화면 중심에 오프셋을 더해서 그리기
            self.image.draw(config.windowWidth // 2 + int(offset_x), config.windowHeight // 2,
                          config.windowWidth, config.windowHeight)
        if self.font:
            # 텍스트도 오프셋 적용
            self.font.draw(config.windowWidth // 2 - 250 + int(offset_x), config.windowHeight // 5 - 100,
                          'PRESS SPACE TO START', (0, 0, 0))

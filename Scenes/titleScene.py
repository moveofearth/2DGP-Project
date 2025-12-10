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

    def play_music(self):
        """타이틀 음악 재생"""
        if self.bgm:
            self.bgm.repeat_play()

    def update(self, deltaTime):
        pass
    def render(self):
        if self.image:
            # 화면 크기에 맞게 스트레치
            self.image.draw(config.windowWidth // 2, config.windowHeight // 2,
                          config.windowWidth, config.windowHeight)
        if self.font:
            # 텍스트 위치
            text_x = config.windowWidth // 2 - 250
            text_y = config.windowHeight // 5 - 100
            text = 'PRESS SPACE TO START'

            # 검은색 테두리 효과 (8방향으로 약간 오프셋된 검은색 텍스트)
            offset = 3
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    if dx != 0 or dy != 0:
                        self.font.draw(text_x + dx, text_y + dy, text, (0, 0, 0))

            # 흰색 텍스트 (위에 그려짐)
            self.font.draw(text_x, text_y, text, (255, 255, 255))

    def render_with_offset(self, offset_x):
        """오프셋을 적용하여 렌더링 (슬라이드 효과용)"""
        if self.image:
            # 화면 중심에 오프셋을 더해서 그리기
            self.image.draw(config.windowWidth // 2 + int(offset_x), config.windowHeight // 2,
                          config.windowWidth, config.windowHeight)

        if self.font:
            # 텍스트 위치 (오프셋 적용)
            text_x = config.windowWidth // 2 - 250 + int(offset_x)
            text_y = config.windowHeight // 5 - 100
            text = 'PRESS SPACE TO START'


            offset = 3
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    if dx != 0 or dy != 0:
                        self.font.draw(text_x + dx, text_y + dy, text, (0, 0, 0))

            # 흰색 텍스트 (위에 그려짐)
            self.font.draw(text_x, text_y, text, (255, 255, 255))

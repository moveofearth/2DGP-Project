import pico2d
import config
import pathlib

class CharacterSelectScene:
    def __init__(self):
        self.characters = ['fighter', 'priest', 'Thief']  # 선택 가능한 캐릭터
        self.p1_index = 0  # 1P 현재 선택 인덱스
        self.p2_index = 0  # 2P 현재 선택 인덱스
        self.p1_selected = False  # 1P 선택 완료 여부
        self.p2_selected = False  # 2P 선택 완료 여부
        self.p1_character = None  # 1P 선택한 캐릭터
        self.p2_character = None  # 2P 선택한 캐릭터

        # 캐릭터 스프라이트
        self.character_sprites = {}
        self.sprite_frames = {}
        self.sprite_frame_index = {}
        self.sprite_animation_time = {}

        # 애니메이션 설정
        self.animation_fps = 10  # 초당 10프레임
        self.frame_time = 1.0 / self.animation_fps

    def initialize(self):
        """캐릭터 선택 스프라이트 로드"""
        for char in self.characters:
            self.character_sprites[char] = []
            path = pathlib.Path.cwd() / 'Resources' / 'Character' / char / 'selected'

            # 해당 폴더의 모든 png 파일 로드
            if path.exists():
                files = sorted([f for f in path.iterdir() if f.suffix == '.png'])
                for file in files:
                    img = pico2d.load_image(str(file))
                    self.character_sprites[char].append(img)

            self.sprite_frames[char] = len(self.character_sprites[char])
            self.sprite_frame_index[char] = 0
            self.sprite_animation_time[char] = 0.0

    def handle_input(self, events):
        """입력 처리"""
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                # 1P 입력 (WASD + Space)
                if not self.p1_selected:
                    if event.key == pico2d.SDLK_a:  # 왼쪽
                        self.p1_index = (self.p1_index - 1) % len(self.characters)
                    elif event.key == pico2d.SDLK_d:  # 오른쪽
                        self.p1_index = (self.p1_index + 1) % len(self.characters)
                    elif event.key == pico2d.SDLK_SPACE:  # 선택
                        self.p1_selected = True
                        self.p1_character = self.characters[self.p1_index]

                # 2P 입력 (방향키 + Enter)
                if not self.p2_selected:
                    if event.key == pico2d.SDLK_LEFT:  # 왼쪽
                        self.p2_index = (self.p2_index - 1) % len(self.characters)
                    elif event.key == pico2d.SDLK_RIGHT:  # 오른쪽
                        self.p2_index = (self.p2_index + 1) % len(self.characters)
                    elif event.key == pico2d.SDLK_RETURN:  # 선택 (Enter)
                        self.p2_selected = True
                        self.p2_character = self.characters[self.p2_index]

    def update(self, deltaTime):
        """애니메이션 업데이트"""
        for char in self.characters:
            if self.sprite_frames[char] > 0:
                self.sprite_animation_time[char] += deltaTime
                if self.sprite_animation_time[char] >= self.frame_time:
                    self.sprite_animation_time[char] = 0.0
                    self.sprite_frame_index[char] = (self.sprite_frame_index[char] + 1) % self.sprite_frames[char]

    def render(self):
        """캐릭터 선택 화면 렌더링"""
        # 배경 (검은색)
        pico2d.clear_canvas()

        # 캐릭터 표시 위치 계산
        char_spacing = config.windowWidth // (len(self.characters) + 1)
        char_y = config.windowHeight // 2

        # 각 캐릭터 스프라이트 그리기
        for i, char in enumerate(self.characters):
            x = char_spacing * (i + 1)

            # 애니메이션 프레임 가져오기
            if self.sprite_frames[char] > 0:
                frame_idx = self.sprite_frame_index[char]
                img = self.character_sprites[char][frame_idx]

                # 스프라이트 크기 조정 (원본의 2배)
                scale = 2.0
                img.draw(x, char_y, img.w * scale, img.h * scale)

        # 1P 선택 표시 (빨간색 테두리)
        if not self.p1_selected:
            p1_x = char_spacing * (self.p1_index + 1)
            self.draw_selection_box(p1_x, char_y, 200, 250, (255, 0, 0))  # 빨간색
        else:
            # 선택 완료 시 선택한 캐릭터 위치에 표시
            p1_selected_x = char_spacing * (self.characters.index(self.p1_character) + 1)
            self.draw_selection_box(p1_selected_x, char_y, 200, 250, (255, 0, 0))

        # 2P 선택 표시 (파란색 테두리)
        if not self.p2_selected:
            p2_x = char_spacing * (self.p2_index + 1)
            self.draw_selection_box(p2_x, char_y, 200, 250, (0, 0, 255))  # 파란색
        else:
            # 선택 완료 시 선택한 캐릭터 위치에 표시
            p2_selected_x = char_spacing * (self.characters.index(self.p2_character) + 1)
            self.draw_selection_box(p2_selected_x, char_y, 200, 250, (0, 0, 255))

        # 안내 텍스트 (선택 키 정보)
        # 간단한 텍스트로 표시

    def draw_selection_box(self, x, y, width, height, color):
        """선택 박스 그리기 (테두리만) - 여러 개의 선으로 두꺼운 테두리 표현"""
        r, g, b = color
        thickness = 3  # 테두리 두께

        # 여러 번 그려서 두꺼운 선 효과
        for i in range(thickness):
            offset = i
            # 위쪽 선
            pico2d.draw_line(
                x - width // 2 - offset, y + height // 2 + offset,
                x + width // 2 + offset, y + height // 2 + offset,
                r, g, b
            )
            # 아래쪽 선
            pico2d.draw_line(
                x - width // 2 - offset, y - height // 2 - offset,
                x + width // 2 + offset, y - height // 2 - offset,
                r, g, b
            )
            # 왼쪽 선
            pico2d.draw_line(
                x - width // 2 - offset, y - height // 2 - offset,
                x - width // 2 - offset, y + height // 2 + offset,
                r, g, b
            )
            # 오른쪽 선
            pico2d.draw_line(
                x + width // 2 + offset, y - height // 2 - offset,
                x + width // 2 + offset, y + height // 2 + offset,
                r, g, b
            )

    def is_both_selected(self):
        """두 플레이어 모두 선택 완료했는지 확인"""
        return self.p1_selected and self.p2_selected

    def get_selected_characters(self):
        """선택된 캐릭터 반환 (p1_character, p2_character)"""
        return self.p1_character, self.p2_character


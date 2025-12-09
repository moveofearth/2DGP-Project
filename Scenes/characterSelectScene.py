import pico2d
import config
import pathlib

class CharacterSelectScene:
    def __init__(self):
        self.characters = ['fighter', 'priest', 'thief']  # 선택 가능한 캐릭터
        self.p1_index = 0  # 1P 현재 선택 인덱스 (fighter)
        self.p2_index = 1  # 2P 현재 선택 인덱스 (priest) - 기본값을 다르게 설정
        self.p1_selected = False  # 1P 선택 완료 여부
        self.p2_selected = False  # 2P 선택 완료 여부
        self.p1_character = None  # 1P 선택한 캐릭터
        self.p2_character = None  # 2P 선택한 캐릭터

        # 배경 이미지
        self.background = None

        # 폰트
        self.font = None

        # 캐릭터 스프라이트
        self.character_sprites = {}
        self.sprite_frames = {}
        self.sprite_frame_index = {}
        self.sprite_animation_time = {}

        # 애니메이션 설정
        self.animation_fps = 10  # 초당 10프레임
        self.frame_time = 1.0 / self.animation_fps

        # 애니메이션 완료 추적
        self.p1_animation_complete = False
        self.p2_animation_complete = False

        # 선택 완료 후 대기 타이머
        self.wait_timer = 0.0
        self.wait_duration = 1.0  # 1초 대기
        self.ready_to_proceed = False  # 플레이씬으로 넘어갈 준비 완료

        # 캐릭터별 Y 오프셋 (선택 시 크게 표시될 때)
        self.character_y_offset = {
            'priest': 100,  # priest를 위로 100픽셀 이동
            'fighter': 0,
            'thief': 50  # thief를 위로 50픽셀 이동
        }

        # 배경음악
        self.bgm = None

    def initialize(self):
        """캐릭터 선택 스프라이트 로드"""
        # 배경 이미지 로드
        background_path = pathlib.Path.cwd() / 'Resources' / 'UI' / 'characterSelect.png'
        if background_path.exists():
            self.background = pico2d.load_image(str(background_path))

        # 폰트 로드
        font_path = pathlib.Path.cwd() / 'ENCR10B.TTF'
        if font_path.exists():
            self.font = pico2d.load_font(str(font_path), 40)

        # 배경음악 로드 (씬 전환 시 재생됨)
        bgm_path = pathlib.Path.cwd() / 'Resources' / 'Sound' / 'SelectMusic.mp3'
        if bgm_path.exists():
            self.bgm = pico2d.load_music(str(bgm_path))
            self.bgm.set_volume(8)

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

    def reset(self):
        """캐릭터 선택 씬 초기화 (재시작용)"""
        self.p1_index = 0
        self.p2_index = 1  # 기본값을 다르게 설정 (priest)
        self.p1_selected = False
        self.p2_selected = False
        self.p1_character = None
        self.p2_character = None
        self.p1_animation_complete = False
        self.p2_animation_complete = False
        self.wait_timer = 0.0
        self.ready_to_proceed = False

        # 모든 캐릭터 애니메이션 리셋
        for char in self.characters:
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
                        # 애니메이션을 처음부터 시작하도록 프레임 인덱스 리셋
                        self.sprite_frame_index[self.p1_character] = 0
                        self.sprite_animation_time[self.p1_character] = 0.0

                # 2P 입력 (방향키 + Enter)
                if not self.p2_selected:
                    if event.key == pico2d.SDLK_LEFT:  # 왼쪽
                        self.p2_index = (self.p2_index - 1) % len(self.characters)
                    elif event.key == pico2d.SDLK_RIGHT:  # 오른쪽
                        self.p2_index = (self.p2_index + 1) % len(self.characters)
                    elif event.key == pico2d.SDLK_RETURN:  # 선택 (Enter)
                        self.p2_selected = True
                        self.p2_character = self.characters[self.p2_index]
                        # 애니메이션을 처음부터 시작하도록 프레임 인덱스 리셋
                        self.sprite_frame_index[self.p2_character] = 0
                        self.sprite_animation_time[self.p2_character] = 0.0

    def update(self, deltaTime):
        """애니메이션 업데이트 - 선택된 캐릭터만 애니메이션"""
        # 1P가 선택한 캐릭터 애니메이션
        if self.p1_selected and self.p1_character and not self.p1_animation_complete:
            char = self.p1_character
            if self.sprite_frames[char] > 0:
                self.sprite_animation_time[char] += deltaTime
                if self.sprite_animation_time[char] >= self.frame_time:
                    self.sprite_animation_time[char] -= self.frame_time  # 수정: 0.0 대신 -= 사용
                    prev_frame = self.sprite_frame_index[char]
                    self.sprite_frame_index[char] = (self.sprite_frame_index[char] + 1) % self.sprite_frames[char]

                    # 애니메이션이 한 바퀴 돌았는지 체크 (마지막 프레임에서 첫 프레임으로)
                    if prev_frame == self.sprite_frames[char] - 1 and self.sprite_frame_index[char] == 0:
                        self.p1_animation_complete = True
                        print("1P animation complete!")

        # 2P가 선택한 캐릭터 애니메이션
        if self.p2_selected and self.p2_character and not self.p2_animation_complete:
            char = self.p2_character
            if self.sprite_frames[char] > 0:
                self.sprite_animation_time[char] += deltaTime
                if self.sprite_animation_time[char] >= self.frame_time:
                    self.sprite_animation_time[char] -= self.frame_time  # 수정: 0.0 대신 -= 사용
                    prev_frame = self.sprite_frame_index[char]
                    self.sprite_frame_index[char] = (self.sprite_frame_index[char] + 1) % self.sprite_frames[char]

                    # 애니메이션이 한 바퀴 돌았는지 체크 (마지막 프레임에서 첫 프레임으로)
                    if prev_frame == self.sprite_frames[char] - 1 and self.sprite_frame_index[char] == 0:
                        self.p2_animation_complete = True
                        print("2P animation complete!")

        # 두 캐릭터 모두 선택되면 1초 대기 후 플레이씬으로 넘어가기
        if self.p1_selected and self.p2_selected and not self.ready_to_proceed:
            self.wait_timer += deltaTime
            if self.wait_timer >= self.wait_duration:
                self.ready_to_proceed = True
                print("Ready to proceed to play scene!")

    def render(self):
        """캐릭터 선택 화면 렌더링"""
        # 배경
        pico2d.clear_canvas()

        # 배경 이미지 그리기
        if self.background:
            self.background.draw(config.windowWidth // 2, config.windowHeight // 2,
                               config.windowWidth, config.windowHeight)

        # 선택할 캐릭터 표시 위치 (아래쪽, 작게)
        char_spacing = config.windowWidth // (len(self.characters) + 1)
        char_y = config.windowHeight // 4  # 화면 하단 1/4 위치
        small_scale = 1.2  # 작은 크기

        # 각 캐릭터 스프라이트 그리기 (선택용, 작게) - 정지 화면
        for i, char in enumerate(self.characters):
            x = char_spacing * (i + 1)

            # 첫 번째 프레임만 표시 (정지 화면)
            if self.sprite_frames[char] > 0:
                img = self.character_sprites[char][0]  # 항상 첫 프레임

                # 스프라이트 크기 조정 (작게)
                img.draw(x, char_y, img.w * small_scale, img.h * small_scale)

        # 1P 선택 표시 (빨간색 테두리) - 하단 선택 영역
        if not self.p1_selected:
            p1_x = char_spacing * (self.p1_index + 1)
            self.draw_selection_box(p1_x - 30, char_y - 20, 140, 170, (255, 0, 0))  # 빨간색, 작게
            # 1P 텍스트 표시 (선택 박스 위)
            if self.font:
                self.font.draw(p1_x - 100, char_y + 105, "1P", (255, 0, 0))
        else:
            # 선택 완료 시 선택한 캐릭터 위치에 표시
            p1_selected_x = char_spacing * (self.characters.index(self.p1_character) + 1)
            self.draw_selection_box(p1_selected_x - 30, char_y - 20, 140, 170, (255, 0, 0))
            # 1P 텍스트 표시 (선택 박스 왼쪽 위)
            if self.font:
                self.font.draw(p1_selected_x - 100, char_y + 105, "1P", (255, 0, 0))

        # 2P 선택 표시 (파란색 테두리) - 하단 선택 영역
        if not self.p2_selected:
            p2_x = char_spacing * (self.p2_index + 1)
            self.draw_selection_box(p2_x - 30, char_y - 20, 150, 180, (0, 0, 255))  # 파란색, 작게
            # 2P 텍스트 표시 (선택 박스 위)
            if self.font:
                self.font.draw(p2_x - 20, char_y + 105, "2P", (0, 0, 255))
        else:
            # 선택 완료 시 선택한 캐릭터 위치에 표시
            p2_selected_x = char_spacing * (self.characters.index(self.p2_character) + 1)
            self.draw_selection_box(p2_selected_x - 30, char_y - 20, 150, 180, (0, 0, 255))
            # 2P 텍스트 표시 (선택 박스 위)
            if self.font:
                self.font.draw(p2_selected_x - 20, char_y + 105, "2P", (0, 0, 255))

        # 선택된 캐릭터를 좌우에 크게 표시
        large_scale = 3.5  # 큰 크기
        side_y = config.windowHeight * 0.8  # 화면 상단 80% 위치

        # 1P 선택 캐릭터 (좌측)
        if self.p1_selected and self.p1_character:
            if self.sprite_frames[self.p1_character] > 0:
                frame_idx = self.sprite_frame_index[self.p1_character]
                img = self.character_sprites[self.p1_character][frame_idx]
                p1_x = config.windowWidth * 0.35  # 좌측 35% 위치 (중심에 더 가깝게)
                # 캐릭터별 Y 오프셋 적용
                y_offset = self.character_y_offset.get(self.p1_character, 0)
                img.draw(p1_x, side_y + y_offset, img.w * large_scale, img.h * large_scale)

        # 2P 선택 캐릭터 (우측, 좌우 반전)
        if self.p2_selected and self.p2_character:
            if self.sprite_frames[self.p2_character] > 0:
                frame_idx = self.sprite_frame_index[self.p2_character]
                img = self.character_sprites[self.p2_character][frame_idx]
                p2_x = config.windowWidth * 0.65  # 우측 65% 위치 (중심에 더 가깝게)
                # 캐릭터별 Y 오프셋 적용
                y_offset = self.character_y_offset.get(self.p2_character, 0)
                # 좌우 반전하여 그리기
                img.clip_composite_draw(
                    0, 0, img.w, img.h,
                    0, 'h',  # 'h'는 수평 반전을 의미
                    p2_x, side_y + y_offset,
                    img.w * large_scale, img.h * large_scale
                )

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
        """두 플레이어 모두 선택 완료하고 1초 대기 후 플레이씬으로 넘어갈 준비가 되었는지 확인"""
        return self.ready_to_proceed

    def get_selected_characters(self):
        """선택된 캐릭터 반환 (p1_character, p2_character)"""
        return self.p1_character, self.p2_character

    def render_with_offset(self, offset_x):
        """오프셋을 적용하여 렌더링 (슬라이드 효과용)"""
        # 배경 이미지 그리기 (오프셋 적용)
        if self.background:
            self.background.draw(config.windowWidth // 2 + int(offset_x), config.windowHeight // 2,
                               config.windowWidth, config.windowHeight)

        # 선택할 캐릭터 표시 위치 (아래쪽, 작게)
        char_spacing = config.windowWidth // (len(self.characters) + 1)
        char_y = config.windowHeight // 4
        small_scale = 1.2

        # 각 캐릭터 스프라이트 그리기 (오프셋 적용)
        for i, char in enumerate(self.characters):
            x = char_spacing * (i + 1) + int(offset_x)
            if self.sprite_frames[char] > 0:
                img = self.character_sprites[char][0]
                img.draw(x, char_y, img.w * small_scale, img.h * small_scale)

        # 1P 선택 표시 (오프셋 적용)
        if not self.p1_selected:
            p1_x = char_spacing * (self.p1_index + 1) + int(offset_x)
            self.draw_selection_box(p1_x - 30, char_y - 20, 140, 170, (255, 0, 0))
            if self.font:
                self.font.draw(p1_x - 100, char_y + 105, "1P", (255, 0, 0))
        else:
            p1_selected_x = char_spacing * (self.characters.index(self.p1_character) + 1) + int(offset_x)
            self.draw_selection_box(p1_selected_x - 30, char_y - 20, 140, 170, (255, 0, 0))
            if self.font:
                self.font.draw(p1_selected_x - 100, char_y + 105, "1P", (255, 0, 0))

        # 2P 선택 표시 (오프셋 적용)
        if not self.p2_selected:
            p2_x = char_spacing * (self.p2_index + 1) + int(offset_x)
            self.draw_selection_box(p2_x - 30, char_y - 20, 150, 180, (0, 0, 255))
            if self.font:
                self.font.draw(p2_x - 20, char_y + 105, "2P", (0, 0, 255))
        else:
            p2_selected_x = char_spacing * (self.characters.index(self.p2_character) + 1) + int(offset_x)
            self.draw_selection_box(p2_selected_x - 30, char_y - 20, 150, 180, (0, 0, 255))
            if self.font:
                self.font.draw(p2_selected_x - 20, char_y + 105, "2P", (0, 0, 255))

        # 선택된 캐릭터를 좌우에 크게 표시 (오프셋 적용)
        large_scale = 3.5
        side_y = config.windowHeight * 0.8

        # 1P 선택 캐릭터
        if self.p1_selected and self.p1_character:
            if self.sprite_frames[self.p1_character] > 0:
                frame_idx = self.sprite_frame_index[self.p1_character]
                img = self.character_sprites[self.p1_character][frame_idx]
                p1_x = config.windowWidth * 0.35 + int(offset_x)
                y_offset = self.character_y_offset.get(self.p1_character, 0)
                img.draw(p1_x, side_y + y_offset, img.w * large_scale, img.h * large_scale)

        # 2P 선택 캐릭터
        if self.p2_selected and self.p2_character:
            if self.sprite_frames[self.p2_character] > 0:
                frame_idx = self.sprite_frame_index[self.p2_character]
                img = self.character_sprites[self.p2_character][frame_idx]
                p2_x = config.windowWidth * 0.65 + int(offset_x)
                y_offset = self.character_y_offset.get(self.p2_character, 0)
                img.clip_composite_draw(
                    0, 0, img.w, img.h,
                    0, 'h',
                    p2_x, side_y + y_offset,
                    img.w * large_scale, img.h * large_scale
                )



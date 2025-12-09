import pico2d
import pathlib

class PlayScene:
    def __init__(self):
        self.background = None
        self.hpbar_bg = None  # HP바 배경
        self.hp_fill = None   # HP바 내부 채우기
        self.count_ui = None
        self.win_count = None  # 승리 카운트 표시
        self.font = None  # 카운트다운용 폰트
        self.small_font = None  # 작은 폰트 (게임 오버 메시지용)
        self.round_over_sound = None  # 라운드 종료 사운드

        # 3판 2선승제 시스템
        self.player1_rounds_won = 0  # Player1 승리 라운드 수
        self.player2_rounds_won = 0  # Player2 승리 라운드 수
        self.max_rounds = 3  # 최대 라운드 수
        self.wins_needed = 2  # 승리에 필요한 라운드 수
        self.game_over = False  # 전체 게임 종료 여부
        self.round_over = False  # 현재 라운드 종료 여부
        self.winner = None  # 최종 승자

        # 카운트다운 시스템
        self.countdown_active = True  # 카운트다운 진행 중 여부
        self.countdown_timer = 0.0  # 카운트다운 타이머
        self.countdown_sequence = ["Ready", "3", "2", "1", "Fight!"]  # 카운트다운 순서
        self.countdown_index = 0  # 현재 카운트다운 인덱스
        self.countdown_duration = 1.0  # 각 카운트당 지속 시간 (초)

    def initialize(self):
        # 플레이 배경 이미지 로딩
        base_path = pathlib.Path.cwd() / 'Resources' / 'Scene'
        self.background = pico2d.load_image(str(base_path / 'stage.png'))

        # HP UI 이미지 로딩
        ui_path = pathlib.Path.cwd() / 'Resources' / 'UI'
        self.hpbar_bg = pico2d.load_image(str(ui_path / 'hpbar.png'))
        self.hp_fill = pico2d.load_image(str(ui_path / 'hp10.png'))
        self.count_ui = pico2d.load_image(str(ui_path / 'count.png'))
        self.win_count = pico2d.load_image(str(ui_path / 'winCount.png'))

        # 폰트 로드 (카운트다운용)
        font_path = pathlib.Path.cwd() / 'ENCR10B.TTF'
        if font_path.exists():
            self.font = pico2d.load_font(str(font_path), 120)
            self.small_font = pico2d.load_font(str(font_path), 50)

        # 라운드 종료 사운드 로드
        round_over_sound_path = pathlib.Path.cwd() / 'Resources' / 'Sound' / 'roundOver.wav'
        if round_over_sound_path.exists():
            self.round_over_sound = pico2d.load_wav(str(round_over_sound_path))
            self.round_over_sound.set_volume(10)

        # 3판 2선승제 초기화
        self.reset_game()

    def reset_game(self):
        """전체 게임 초기화"""
        self.player1_rounds_won = 0
        self.player2_rounds_won = 0
        self.game_over = False
        self.round_over = False
        self.winner = None

    def reset_round(self):
        """라운드 초기화"""
        self.round_over = False
        # 카운트다운 재시작
        self.start_countdown()

    def start_countdown(self):
        """카운트다운 시작"""
        self.countdown_active = True
        self.countdown_timer = 0.0
        self.countdown_index = 0

    def check_round_end(self, player1_hp, player2_hp):
        """라운드 종료 체크 및 승자 결정"""
        if self.round_over or self.game_over:
            return

        # 어느 한 플레이어의 HP가 0이하면 라운드 종료
        if player1_hp <= 0:
            self.player2_rounds_won += 1
            self.round_over = True
            # 라운드 종료 사운드 재생
            if self.round_over_sound:
                self.round_over_sound.play()
            print(f"Player2 wins round! Score: P1({self.player1_rounds_won}) - P2({self.player2_rounds_won})")
            self.check_game_end()
        elif player2_hp <= 0:
            self.player1_rounds_won += 1
            self.round_over = True
            # 라운드 종료 사운드 재생
            if self.round_over_sound:
                self.round_over_sound.play()
            print(f"Player1 wins round! Score: P1({self.player1_rounds_won}) - P2({self.player2_rounds_won})")
            self.check_game_end()

    def check_game_end(self):
        """전체 게임 종료 체크"""
        if self.player1_rounds_won >= self.wins_needed:
            self.game_over = True
            self.winner = "Player1"
            print(f"Game Over! {self.winner} wins the match!")
        elif self.player2_rounds_won >= self.wins_needed:
            self.game_over = True
            self.winner = "Player2"
            print(f"Game Over! {self.winner} wins the match!")

    def is_game_over(self):
        """게임 종료 여부 반환"""
        return self.game_over

    def is_round_over(self):
        """라운드 종료 여부 반환"""
        return self.round_over

    def get_winner(self):
        """최종 승자 반환"""
        return self.winner

    def is_countdown_active(self):
        """카운트다운 진행 중 여부 반환"""
        return self.countdown_active

    def update(self, deltaTime):
        # 카운트다운 업데이트
        if self.countdown_active:
            self.countdown_timer += deltaTime
            if self.countdown_timer >= self.countdown_duration:
                self.countdown_timer = 0.0
                self.countdown_index += 1
                # 모든 카운트다운 완료
                if self.countdown_index >= len(self.countdown_sequence):
                    self.countdown_active = False
                    self.countdown_index = 0

    def render(self, player1_hp=100, player1_max_hp=100, player2_hp=100, player2_max_hp=100):
        """HP 정보를 받아서 렌더링"""
        if self.background:
            # 배경을 2배 스케일링하여 전체 화면에 맞춤 (960x540 -> 1920x1080)
            self.background.draw(960, 540, self.background.w * 2, self.background.h * 2)
        else:
            print("WARNING: Background is None in render!")

        # HP바 렌더링 (hpbar.png와 hp10.png 사용)
        if self.hpbar_bg and self.hp_fill:
            # Player1 HP바 (좌측 상단)
            hpbar_x = 480  # 350에서 480으로 이동 (중앙에 더 가깝게)
            hpbar_y = 1000
            hpbar_scale = 1.12  # 1.4에서 1.12로 감소 (20% 추가 감소)
            hp_segments = 10  # HP 세그먼트 개수

            # HP바 배경
            self.hpbar_bg.draw(hpbar_x, hpbar_y, self.hpbar_bg.w * hpbar_scale, self.hpbar_bg.h * hpbar_scale)

            # HP바 채우기 (10개의 hp10 세그먼트로 표시)
            # 각 세그먼트는 HP 10을 나타냄 (총 HP 100)
            # HP 바 내부 영역 계산 (패딩 고려)
            hpbar_inner_width = self.hpbar_bg.w * hpbar_scale - 20  # 양쪽 패딩 10씩
            hp_segment_width = hpbar_inner_width / hp_segments  # 각 세그먼트의 너비
            hp_segment_height = self.hp_fill.h * hpbar_scale

            # HP 계산 (0-100 범위로 클램프)
            current_hp1 = max(0, min(player1_max_hp, player1_hp))
            hp_segments_to_show = int(current_hp1 / 10)  # 완전히 채워진 세그먼트 수
            partial_hp = current_hp1 % 10  # 부분적으로 채워진 세그먼트의 HP

            # HP바의 시작 위치 계산 (왼쪽 정렬, 패딩 고려)
            hp_start_x = hpbar_x - (self.hpbar_bg.w * hpbar_scale) / 2 + 10 + hp_segment_width / 2

            # 완전히 채워진 세그먼트 그리기
            for i in range(hp_segments_to_show):
                segment_x = hp_start_x + i * hp_segment_width
                # hp10 이미지를 세그먼트 너비에 맞게 스케일링
                segment_scale = hp_segment_width / self.hp_fill.w
                self.hp_fill.draw(segment_x, hpbar_y,
                                self.hp_fill.w * segment_scale,
                                self.hp_fill.h * hpbar_scale)

            # 부분적으로 채워진 세그먼트 그리기
            if partial_hp > 0 and hp_segments_to_show < hp_segments:
                segment_x = hp_start_x + hp_segments_to_show * hp_segment_width
                partial_ratio = partial_hp / 10.0
                partial_width = int(self.hp_fill.w * partial_ratio)
                segment_scale = hp_segment_width / self.hp_fill.w

                if partial_width > 0:
                    self.hp_fill.clip_draw(
                        0, 0, partial_width, self.hp_fill.h,
                        segment_x - hp_segment_width / 2 + (partial_width * segment_scale) / 2,
                        hpbar_y,
                        partial_width * segment_scale,
                        self.hp_fill.h * hpbar_scale
                    )

            # Player2 HP바 (우측 상단, 좌우 반전)
            hpbar_x2 = 1440  # 1570에서 1440으로 이동 (중앙에 더 가깝게)

            # HP바 배경 (좌우 반전)
            self.hpbar_bg.clip_composite_draw(
                0, 0, self.hpbar_bg.w, self.hpbar_bg.h,
                0, 'h',
                hpbar_x2, hpbar_y,
                self.hpbar_bg.w * hpbar_scale, self.hpbar_bg.h * hpbar_scale
            )

            # HP바 채우기 (10개의 hp10 세그먼트로 표시, 좌우 반전)
            # HP 계산 (0-100 범위로 클램프)
            current_hp2 = max(0, min(player2_max_hp, player2_hp))
            hp_segments_to_show2 = int(current_hp2 / 10)  # 완전히 채워진 세그먼트 수
            partial_hp2 = current_hp2 % 10  # 부분적으로 채워진 세그먼트의 HP

            # HP바의 시작 위치 계산 (오른쪽 정렬, 패딩 고려)
            hp_start_x2 = hpbar_x2 + (self.hpbar_bg.w * hpbar_scale) / 2 - 10 - hp_segment_width / 2

            # 완전히 채워진 세그먼트 그리기 (좌우 반전)
            for i in range(hp_segments_to_show2):
                segment_x2 = hp_start_x2 - i * hp_segment_width
                segment_scale = hp_segment_width / self.hp_fill.w
                self.hp_fill.clip_composite_draw(
                    0, 0, self.hp_fill.w, self.hp_fill.h,
                    0, 'h',
                    segment_x2, hpbar_y,
                    self.hp_fill.w * segment_scale,
                    self.hp_fill.h * hpbar_scale
                )

            # 부분적으로 채워진 세그먼트 그리기 (좌우 반전)
            if partial_hp2 > 0 and hp_segments_to_show2 < hp_segments:
                segment_x2 = hp_start_x2 - hp_segments_to_show2 * hp_segment_width
                partial_ratio2 = partial_hp2 / 10.0
                partial_width2 = int(self.hp_fill.w * partial_ratio2)
                segment_scale = hp_segment_width / self.hp_fill.w

                if partial_width2 > 0:
                    self.hp_fill.clip_composite_draw(
                        self.hp_fill.w - partial_width2, 0, partial_width2, self.hp_fill.h,
                        0, 'h',
                        segment_x2 + hp_segment_width / 2 - (partial_width2 * segment_scale) / 2,
                        hpbar_y,
                        partial_width2 * segment_scale,
                        self.hp_fill.h * hpbar_scale
                    )

        # Count UI 렌더링 - 각 플레이어 2개씩
        if self.count_ui and self.win_count:
            scaled_count_width = self.count_ui.w * 0.84  # 1.5에서 0.84로 감소 (HP바와 동일한 44% 감소)
            scaled_count_height = self.count_ui.h * 0.84
            count_spacing = scaled_count_width + 10

            # Player1 카운트 (좌측 상단)
            count_start_x1 = 200  # 80에서 200으로 이동 (중앙에 더 가깝게)
            count_y = 950  # 900에서 950으로 이동 (HP바에 더 가깝게)

            for i in range(2):
                # Count 배경
                self.count_ui.draw(count_start_x1 + i * count_spacing, count_y,
                                 scaled_count_width, scaled_count_height)

                # 승리한 라운드 수만큼 winCount 표시
                if i < self.player1_rounds_won:
                    self.win_count.draw(count_start_x1 + i * count_spacing, count_y,
                                      scaled_count_width, scaled_count_height)

            # Player2 카운트 (우측 상단, 좌우 반전)
            count_start_x2 = 1720  # 1840에서 1720으로 이동 (중앙에 더 가깝게)

            for i in range(2):
                # Count 배경 (좌우 반전)
                self.count_ui.clip_composite_draw(
                    0, 0, self.count_ui.w, self.count_ui.h,
                    0, 'h',
                    count_start_x2 - i * count_spacing, count_y,
                    scaled_count_width, scaled_count_height
                )

                # 승리한 라운드 수만큼 winCount 표시 (좌우 반전)
                if i < self.player2_rounds_won:
                    self.win_count.clip_composite_draw(
                        0, 0, self.win_count.w, self.win_count.h,
                        0, 'h',
                        count_start_x2 - i * count_spacing, count_y,
                        scaled_count_width, scaled_count_height
                    )

        # 카운트다운 텍스트 렌더링 (화면 중앙, 노란색)
        if self.countdown_active and self.font:
            if self.countdown_index < len(self.countdown_sequence):
                text = self.countdown_sequence[self.countdown_index]
                # 텍스트 길이에 따라 x 위치 조정 (대략적인 중앙 정렬)
                text_width = len(text) * 60  # 폰트 크기 120의 절반 정도로 추정
                center_x = 960 - text_width // 2
                # 화면 중앙에 노란색으로 표시
                self.font.draw(center_x, 540, text, (255, 255, 0))

        # 게임 오버 시 승자 표시 (화면 중앙, 노란색)
        if self.game_over and self.font and self.winner:
            win_text = f"{self.winner} WIN!"
            # 텍스트 길이에 따라 x 위치 조정
            text_width = len(win_text) * 60
            center_x = 960 - text_width // 2
            # 화면 중앙에 노란색으로 표시
            self.font.draw(center_x, 600, win_text, (255, 255, 0))
            # "Press SPACE to continue" 메시지
            if self.small_font:
                continue_text = "Press SPACE to continue"
                continue_width = len(continue_text) * 25
                continue_x = 960 - continue_width // 2
                self.small_font.draw(continue_x, 480, continue_text, (255, 255, 0))

    def render_with_offset(self, offset_x, player1_hp=100, player1_max_hp=100, player2_hp=100, player2_max_hp=100):
        """오프셋을 적용하여 렌더링 (슬라이드 효과용)"""
        # 배경 오프셋 적용
        if self.background:
            self.background.draw(960 + int(offset_x), 540, self.background.w * 2, self.background.h * 2)

        # HP바와 UI는 화면에 고정 (오프셋 적용하지 않음)
        # HP바 렌더링
        if self.hpbar_bg and self.hp_fill:
            # Player1 HP바 (좌측 상단)
            hpbar_x = 480
            hpbar_y = 1000
            hpbar_scale = 1.12
            hp_segments = 10

            # HP바 배경
            self.hpbar_bg.draw(hpbar_x, hpbar_y, self.hpbar_bg.w * hpbar_scale, self.hpbar_bg.h * hpbar_scale)

            # HP바 채우기
            hpbar_inner_width = self.hpbar_bg.w * hpbar_scale - 20
            hp_segment_width = hpbar_inner_width / hp_segments
            hp_segment_height = self.hp_fill.h * hpbar_scale

            current_hp1 = max(0, min(player1_max_hp, player1_hp))
            hp_segments_to_show = int(current_hp1 / 10)
            partial_hp = current_hp1 % 10

            hp_start_x = hpbar_x - (self.hpbar_bg.w * hpbar_scale) / 2 + 10 + hp_segment_width / 2

            for i in range(hp_segments_to_show):
                segment_x = hp_start_x + i * hp_segment_width
                segment_scale = hp_segment_width / self.hp_fill.w
                self.hp_fill.draw(segment_x, hpbar_y,
                                self.hp_fill.w * segment_scale,
                                self.hp_fill.h * hpbar_scale)

            if partial_hp > 0 and hp_segments_to_show < hp_segments:
                segment_x = hp_start_x + hp_segments_to_show * hp_segment_width
                partial_ratio = partial_hp / 10.0
                partial_width = int(self.hp_fill.w * partial_ratio)
                segment_scale = hp_segment_width / self.hp_fill.w

                if partial_width > 0:
                    self.hp_fill.clip_draw(
                        0, 0, partial_width, self.hp_fill.h,
                        segment_x - hp_segment_width / 2 + (partial_width * segment_scale) / 2,
                        hpbar_y,
                        partial_width * segment_scale,
                        self.hp_fill.h * hpbar_scale
                    )

            # Player2 HP바 (우측 상단, 좌우 반전)
            hpbar_x2 = 1440

            self.hpbar_bg.clip_composite_draw(
                0, 0, self.hpbar_bg.w, self.hpbar_bg.h,
                0, 'h',
                hpbar_x2, hpbar_y,
                self.hpbar_bg.w * hpbar_scale, self.hpbar_bg.h * hpbar_scale
            )

            current_hp2 = max(0, min(player2_max_hp, player2_hp))
            hp_segments_to_show2 = int(current_hp2 / 10)
            partial_hp2 = current_hp2 % 10

            hp_start_x2 = hpbar_x2 + (self.hpbar_bg.w * hpbar_scale) / 2 - 10 - hp_segment_width / 2

            for i in range(hp_segments_to_show2):
                segment_x2 = hp_start_x2 - i * hp_segment_width
                segment_scale = hp_segment_width / self.hp_fill.w
                self.hp_fill.clip_composite_draw(
                    0, 0, self.hp_fill.w, self.hp_fill.h,
                    0, 'h',
                    segment_x2, hpbar_y,
                    self.hp_fill.w * segment_scale,
                    self.hp_fill.h * hpbar_scale
                )

            if partial_hp2 > 0 and hp_segments_to_show2 < hp_segments:
                segment_x2 = hp_start_x2 - hp_segments_to_show2 * hp_segment_width
                partial_ratio2 = partial_hp2 / 10.0
                partial_width2 = int(self.hp_fill.w * partial_ratio2)
                segment_scale = hp_segment_width / self.hp_fill.w

                if partial_width2 > 0:
                    self.hp_fill.clip_composite_draw(
                        self.hp_fill.w - partial_width2, 0, partial_width2, self.hp_fill.h,
                        0, 'h',
                        segment_x2 + hp_segment_width / 2 - (partial_width2 * segment_scale) / 2,
                        hpbar_y,
                        partial_width2 * segment_scale,
                        self.hp_fill.h * hpbar_scale
                    )

        # Count UI 렌더링
        if self.count_ui and self.win_count:
            scaled_count_width = self.count_ui.w * 0.84
            scaled_count_height = self.count_ui.h * 0.84
            count_spacing = scaled_count_width + 10

            count_start_x1 = 200
            count_y = 950

            for i in range(2):
                self.count_ui.draw(count_start_x1 + i * count_spacing, count_y,
                                 scaled_count_width, scaled_count_height)
                if i < self.player1_rounds_won:
                    self.win_count.draw(count_start_x1 + i * count_spacing, count_y,
                                      scaled_count_width, scaled_count_height)

            count_start_x2 = 1720

            for i in range(2):
                self.count_ui.clip_composite_draw(
                    0, 0, self.count_ui.w, self.count_ui.h,
                    0, 'h',
                    count_start_x2 - i * count_spacing, count_y,
                    scaled_count_width, scaled_count_height
                )
                if i < self.player2_rounds_won:
                    self.win_count.clip_composite_draw(
                        0, 0, self.win_count.w, self.win_count.h,
                        0, 'h',
                        count_start_x2 - i * count_spacing, count_y,
                        scaled_count_width, scaled_count_height
                    )

        # 카운트다운 텍스트 렌더링
        if self.countdown_active and self.font:
            if self.countdown_index < len(self.countdown_sequence):
                text = self.countdown_sequence[self.countdown_index]
                text_width = len(text) * 60
                center_x = 960 - text_width // 2
                self.font.draw(center_x, 540, text, (255, 255, 0))

        # 게임 오버 시 승자 표시
        if self.game_over and self.font and self.winner:
            win_text = f"{self.winner} WIN!"
            text_width = len(win_text) * 60
            center_x = 960 - text_width // 2
            self.font.draw(center_x, 600, win_text, (255, 255, 0))
            if self.small_font:
                continue_text = "Press SPACE to continue"
                continue_width = len(continue_text) * 25
                continue_x = 960 - continue_width // 2
                self.small_font.draw(continue_x, 480, continue_text, (255, 255, 0))


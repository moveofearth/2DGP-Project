import pico2d
from Scenes import titleScene
from Scenes import playScene
from Scenes import characterSelectScene
import config


class SceneManager:
    def __init__(self):
        self.current_scene = 'title'  # 'title', 'character_select', 'play'
        self.title_scene = titleScene.TitleScene()
        self.character_select_scene = characterSelectScene.CharacterSelectScene()
        self.play_scene = playScene.PlayScene()

        # 씬 전환 슬라이드 효과 관련
        self.is_transitioning = False
        self.transition_duration = 0.5  # 전환 시간 (초)
        self.transition_timer = 0.0
        self.transition_from = None
        self.transition_to = None
        self.transition_offset = 0.0  # 슬라이드 오프셋

    def initialize(self):
        self.title_scene.initialize()
        self.character_select_scene.initialize()
        self.play_scene.initialize()

    def change_to_character_select(self):
        """캐릭터 선택 씬으로 전환"""
        self.character_select_scene.reset()  # 씬 리셋
        self.start_transition('title', 'character_select')

    def change_to_play_scene(self):
        """플레이 씬으로 전환"""
        self.start_transition('character_select', 'play')

    def is_title_scene(self):
        """현재 타이틀 씬인지 확인"""
        return self.current_scene == 'title'

    def is_character_select_scene(self):
        """현재 캐릭터 선택 씬인지 확인"""
        return self.current_scene == 'character_select'

    def start_transition(self, from_scene, to_scene):
        """씬 전환 시작"""
        self.is_transitioning = True
        self.transition_timer = 0.0
        self.transition_from = from_scene
        self.transition_to = to_scene
        self.transition_offset = 0.0
        # 씬을 즉시 전환 (로직은 새 씬에서 동작하도록)
        self.current_scene = to_scene

    def update(self, deltaTime):
        # 전환 중일 때
        if self.is_transitioning:
            self.transition_timer += deltaTime
            # 전환 진행도 계산 (0.0 ~ 1.0)
            progress = min(self.transition_timer / self.transition_duration, 1.0)
            # 이징 함수 적용 (부드러운 전환)
            self.transition_offset = self._ease_out_cubic(progress)

            # 전환 중인 양쪽 씬 모두 업데이트 (애니메이션 유지)
            if self.transition_from == 'title':
                self.title_scene.update(deltaTime)
            elif self.transition_from == 'character_select':
                self.character_select_scene.update(deltaTime)
            elif self.transition_from == 'play':
                self.play_scene.update(deltaTime)

            if self.transition_to == 'title':
                self.title_scene.update(deltaTime)
            elif self.transition_to == 'character_select':
                self.character_select_scene.update(deltaTime)
            elif self.transition_to == 'play':
                self.play_scene.update(deltaTime)

            # 전환 완료
            if progress >= 1.0:
                self.is_transitioning = False
                self.transition_from = None
                self.transition_to = None
                self.transition_offset = 0.0
        else:
            # 현재 씬 업데이트
            if self.current_scene == 'title':
                self.title_scene.update(deltaTime)
            elif self.current_scene == 'character_select':
                self.character_select_scene.update(deltaTime)
            elif self.current_scene == 'play':
                self.play_scene.update(deltaTime)

    def _ease_out_cubic(self, t):
        """부드러운 이징 함수"""
        return 1 - pow(1 - t, 3)

    def render(self):
        pico2d.clear_canvas()

        # 전환 중일 때
        if self.is_transitioning:
            # 이전 씬은 왼쪽으로 이동
            from_offset_x = -config.windowWidth * self.transition_offset
            # 다음 씬은 오른쪽에서 왼쪽으로 이동
            to_offset_x = config.windowWidth * (1.0 - self.transition_offset)

            # 이전 씬 렌더링 (왼쪽으로 슬라이드)
            self._render_scene_with_offset(self.transition_from, from_offset_x)
            # 다음 씬 렌더링 (오른쪽에서 들어옴)
            self._render_scene_with_offset(self.transition_to, to_offset_x)
        else:
            # 일반 렌더링
            if self.current_scene == 'title':
                self.title_scene.render()
            elif self.current_scene == 'character_select':
                self.character_select_scene.render()
            elif self.current_scene == 'play':
                self.play_scene.render()

    def _render_scene_with_offset(self, scene_name, offset_x):
        """씬을 오프셋을 적용하여 렌더링"""
        if scene_name == 'title':
            self._render_with_clip(self.title_scene, offset_x)
        elif scene_name == 'character_select':
            self._render_with_clip(self.character_select_scene, offset_x)
        elif scene_name == 'play':
            self._render_with_clip(self.play_scene, offset_x)

    def _render_with_clip(self, scene, offset_x):
        """클리핑 영역을 설정하고 씬 렌더링"""
        # 임시 캔버스 생성은 pico2d에서 직접 지원하지 않으므로
        # 각 씬의 이미지를 오프셋을 적용하여 그리도록 수정
        if hasattr(scene, 'render_with_offset'):
            scene.render_with_offset(offset_x)
        else:
            # 기본 렌더링 (오프셋 적용을 위해 각 씬에 메서드 추가 필요)
            scene.render()

    def get_character_select_scene(self):
        """캐릭터 선택 씬 반환"""
        return self.character_select_scene

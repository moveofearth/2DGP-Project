import pico2d

class IOManager:
    def __init__(self):
        self.player1_keys = {'w': False, 's': False, 'a': False, 'd': False, 'f': False, 'g': False}
        self.player2_keys = {'up': False, 'down': False, 'left': False, 'right': False, 'one': False, 'two': False}
        # 연계 공격을 위한 입력 버퍼
        self.player1_combo_input = False
        self.player2_combo_input = False

    def handleMoveInputPlayer1(self, events):
        # 이벤트로 키 상태 업데이트
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_w:
                    self.player1_keys['w'] = True
                elif event.key == pico2d.SDLK_s:
                    self.player1_keys['s'] = True
                elif event.key == pico2d.SDLK_a:
                    self.player1_keys['a'] = True
                elif event.key == pico2d.SDLK_d:
                    self.player1_keys['d'] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_w:
                    self.player1_keys['w'] = False
                elif event.key == pico2d.SDLK_s:
                    self.player1_keys['s'] = False
                elif event.key == pico2d.SDLK_a:
                    self.player1_keys['a'] = False
                elif event.key == pico2d.SDLK_d:
                    self.player1_keys['d'] = False

        # 현재 눌린 이동 키 상태에 따라 방향 반환
        if self.player1_keys['w']:
            return 'up'
        elif self.player1_keys['s']:
            return 'down'
        elif self.player1_keys['a']:
            return 'left'
        elif self.player1_keys['d']:
            return 'right'

        return None

    def handleATKInputPlayer1(self, events):
        # 공격 키 이벤트 처리
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_f:
                    self.player1_keys['f'] = True
                if event.key == pico2d.SDLK_g:
                    self.player1_keys['g'] = True
                    # strongMiddleATK 중 추가 입력 감지
                    self.player1_combo_input = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_f:
                    self.player1_keys['f'] = False
                if event.key == pico2d.SDLK_g:
                    self.player1_keys['g'] = False

        # 공격키 조합 확인
        if self.player1_keys['f']:
            return 'fastMiddleATK'
        elif self.player1_keys['g']:
            # up/down 키와 조합 확인
            if self.player1_keys['w']:
                return 'strongUpperATK'
            elif self.player1_keys['s']:
                return 'strongLowerATK'
            else:
                return 'strongMiddleATK'

        return None

    def check_player1_combo_input(self):
        """Player1의 연계 입력 확인 및 리셋"""
        if self.player1_combo_input:
            self.player1_combo_input = False
            return True
        return False

    def handleMoveInputPlayer2(self, events):
        # 이벤트로 키 상태 업데이트
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_UP:
                    self.player2_keys['up'] = True
                elif event.key == pico2d.SDLK_DOWN:
                    self.player2_keys['down'] = True
                elif event.key == pico2d.SDLK_LEFT:
                    self.player2_keys['left'] = True
                elif event.key == pico2d.SDLK_RIGHT:
                    self.player2_keys['right'] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_UP:
                    self.player2_keys['up'] = False
                elif event.key == pico2d.SDLK_DOWN:
                    self.player2_keys['down'] = False
                elif event.key == pico2d.SDLK_LEFT:
                    self.player2_keys['left'] = False
                elif event.key == pico2d.SDLK_RIGHT:
                    self.player2_keys['right'] = False

        # 현재 눌린 이동 키 상태에 따라 방향 반환
        if self.player2_keys['up']:
            return 'up'
        elif self.player2_keys['down']:
            return 'down'
        elif self.player2_keys['left']:
            return 'left'
        elif self.player2_keys['right']:
            return 'right'

        return None

    def handleATKInputPlayer2(self, events):
        # 공격 키 이벤트 처리
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_KP_1:
                    self.player2_keys['one'] = True
                if event.key == pico2d.SDLK_KP_2:
                    self.player2_keys['two'] = True
                    # strongMiddleATK 중 추가 입력 감지
                    self.player2_combo_input = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_KP_1:
                    self.player2_keys['one'] = False
                if event.key == pico2d.SDLK_KP_2:
                    self.player2_keys['two'] = False

        # 공격키 조합 확인
        if self.player2_keys['one']:
            return 'fastMiddleATK'
        elif self.player2_keys['two']:
            # up/down 키와 조합 확인
            if self.player2_keys['up']:
                return 'strongUpperATK'
            elif self.player2_keys['down']:
                return 'strongLowerATK'
            else:
                return 'strongMiddleATK'

        return None

    def check_player2_combo_input(self):
        """Player2의 연계 입력 확인 및 리셋"""
        if self.player2_combo_input:
            self.player2_combo_input = False
            return True
        return False

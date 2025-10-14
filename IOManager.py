import pico2d

class IOManager:
    def __init__(self):
        self.player1_keys = {'w': False, 's': False, 'a': False, 'd': False, 'f': False}
        self.player2_keys = {'up': False, 'down': False, 'left': False, 'right': False, 'zero': False}

    def handleInputPlayer1(self, events):
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
                elif event.key == pico2d.SDLK_f:
                    self.player1_keys['f'] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_w:
                    self.player1_keys['w'] = False
                elif event.key == pico2d.SDLK_s:
                    self.player1_keys['s'] = False
                elif event.key == pico2d.SDLK_a:
                    self.player1_keys['a'] = False
                elif event.key == pico2d.SDLK_d:
                    self.player1_keys['d'] = False

        # 현재 눌린 키 상태에 따라 방향 반환
        if self.player1_keys['w']:
            return 'up'
        elif self.player1_keys['s']:
            return 'down'
        elif self.player1_keys['a']:
            return 'left'
        elif self.player1_keys['d']:
            return 'right'
        elif self.player1_keys['f']:
            return 'fastMiddleATK'

        return None

    def handleInputPlayer2(self, events):
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
                elif event.key == pico2d.SDLK_0:
                    self.player1_keys['zero'] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_UP:
                    self.player2_keys['up'] = False
                elif event.key == pico2d.SDLK_DOWN:
                    self.player2_keys['down'] = False
                elif event.key == pico2d.SDLK_LEFT:
                    self.player2_keys['left'] = False
                elif event.key == pico2d.SDLK_RIGHT:
                    self.player2_keys['right'] = False

        # 현재 눌린 키 상태에 따라 방향 반환
        if self.player2_keys['up']:
            return 'up'
        elif self.player2_keys['down']:
            return 'down'
        elif self.player2_keys['left']:
            return 'left'
        elif self.player2_keys['right']:
            return 'right'
        elif self.player2_keys['zero']:
            return 'fastMiddleATK'

        return None

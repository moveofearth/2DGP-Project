import pico2d

class IOManager:
    def __init__(self):
        self.player1_keys = {'w': False, 's': False, 'a': False, 'd': False, 'f': False, 'g': False, 'h': False}
        self.player2_keys = {'up': False, 'down': False, 'left': False, 'right': False, 'ctrl': False, 'shift': False, 'three': False}
        # 연계 공격을 위한 입력 버퍼
        self.player1_combo_input = False
        self.player2_combo_input = False

    def handleSpaceInput(self, events):
        """스페이스바 입력 처리"""
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_SPACE:
                    return True
        return False

    def handleCharacterChangePlayer1(self, events):
        """Player1의 캐릭터 변경 입력 처리"""
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_1:
                    return 'priest'
                elif event.key == pico2d.SDLK_2:
                    return 'thief'
                elif event.key == pico2d.SDLK_3:
                    return 'fighter'
        return None

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
                    # F키로 모든 연계 공격 처리 (thief의 fastMiddleATK와 strongMiddleATK 연계)
                    self.player1_combo_input = True
                if event.key == pico2d.SDLK_g:
                    self.player1_keys['g'] = True
                    # G키는 priest의 strongMiddleATK 연계만 처리
                    self.player1_combo_input = True
                if event.key == pico2d.SDLK_h:
                    self.player1_keys['h'] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_f:
                    self.player1_keys['f'] = False
                if event.key == pico2d.SDLK_g:
                    self.player1_keys['g'] = False
                if event.key == pico2d.SDLK_h:
                    self.player1_keys['h'] = False

        # rage 스킬 체크 (가장 우선순위)
        if self.player1_keys['h']:
            return 'rageSkill'

        # 공격키 조합 확인
        if self.player1_keys['f']:
            # w/s키와 조합 확인
            if self.player1_keys['w']:
                return 'fastUpperATK'
            elif self.player1_keys['s']:
                return 'fastLowerATK'
            else:
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

    def check_player1_combo_input(self, current_state):
        """Player1의 연계 입력 확인 및 리셋 - 정확한 키 조합 체크"""
        if not self.player1_combo_input:
            return None

        self.player1_combo_input = False

        # 현재 공격 상태에 따라 필요한 키 조합 체크
        # 중단 공격 연계: 위/아래 키 없이 같은 공격 키
        if current_state == 'fastMiddleATK' or current_state == 'fastMiddleATK2':
            # F키만 눌려있고 W/S는 안눌려있어야 함
            if self.player1_keys['f'] and not self.player1_keys['w'] and not self.player1_keys['s']:
                return 'fastMiddleATK_combo'
        elif current_state == 'strongMiddleATK':
            # G키만 눌려있고 W/S는 안눌려있어야 함
            if self.player1_keys['g'] and not self.player1_keys['w'] and not self.player1_keys['s']:
                return 'strongMiddleATK_combo'
        # 상단 공격 연계: W키 + 같은 공격 키
        elif current_state == 'strongUpperATK':
            # W + G키가 눌려있어야 함
            if self.player1_keys['g'] and self.player1_keys['w']:
                return 'strongUpperATK_combo'

        return None

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
                if event.key == pico2d.SDLK_RCTRL or event.key == pico2d.SDLK_LCTRL:
                    self.player2_keys['ctrl'] = True
                    # Ctrl키로 모든 연계 공격 처리 (thief의 fastMiddleATK와 strongMiddleATK 연계)
                    self.player2_combo_input = True
                if event.key == pico2d.SDLK_RSHIFT or event.key == pico2d.SDLK_LSHIFT:
                    self.player2_keys['shift'] = True
                    # Shift키는 priest의 strongMiddleATK 연계만 처리
                    self.player2_combo_input = True
                if event.key == pico2d.SDLK_KP_3:
                    self.player2_keys['three'] = True
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_RCTRL or event.key == pico2d.SDLK_LCTRL:
                    self.player2_keys['ctrl'] = False
                if event.key == pico2d.SDLK_RSHIFT or event.key == pico2d.SDLK_LSHIFT:
                    self.player2_keys['shift'] = False
                if event.key == pico2d.SDLK_KP_3:
                    self.player2_keys['three'] = False


        # 공격키 조합 확인
        if self.player2_keys['ctrl']:
            # up/down키와 조합 확인
            if self.player2_keys['up']:
                return 'fastUpperATK'
            elif self.player2_keys['down']:
                return 'fastLowerATK'
            else:
                return 'fastMiddleATK'
        elif self.player2_keys['shift']:
            # up/down 키와 조합 확인
            if self.player2_keys['up']:
                return 'strongUpperATK'
            elif self.player2_keys['down']:
                return 'strongLowerATK'
            else:
                return 'strongMiddleATK'

        return None

    def check_player2_combo_input(self, current_state):
        """Player2의 연계 입력 확인 및 리셋 - 정확한 키 조합 체크"""
        if not self.player2_combo_input:
            return None

        self.player2_combo_input = False

        # 현재 공격 상태에 따라 필요한 키 조합 체크
        # 중단 공격 연계: 위/아래 키 없이 같은 공격 키
        if current_state == 'fastMiddleATK' or current_state == 'fastMiddleATK2':
            # Ctrl키만 눌려있고 UP/DOWN은 안눌려있어야 함
            if self.player2_keys['ctrl'] and not self.player2_keys['up'] and not self.player2_keys['down']:
                return 'fastMiddleATK_combo'
        elif current_state == 'strongMiddleATK':
            # Shift키만 눌려있고 UP/DOWN은 안눌려있어야 함
            if self.player2_keys['shift'] and not self.player2_keys['up'] and not self.player2_keys['down']:
                return 'strongMiddleATK_combo'
        # 상단 공격 연계: UP키 + 같은 공격 키
        elif current_state == 'strongUpperATK':
            # UP + Shift키가 눌려있어야 함
            if self.player2_keys['shift'] and self.player2_keys['up']:
                return 'strongUpperATK_combo'

        return None

    def get_player1_position_state(self):
        """Player1의 위치 상태 반환 (High, Middle, Low)"""
        if self.player1_keys['w']:
            return 'High'
        elif self.player1_keys['s']:
            return 'Low'
        else:
            return 'Middle'

    def get_player2_position_state(self):
        """Player2의 위치 상태 반환 (High, Middle, Low)"""
        if self.player2_keys['up']:
            return 'High'
        elif self.player2_keys['down']:
            return 'Low'
        else:
            return 'Middle'

    def check_player1_getup_input(self):
        """Player1의 기상 입력 확인 (방향키 중 아무거나)"""
        return (self.player1_keys['w'] or self.player1_keys['a'] or
                self.player1_keys['s'] or self.player1_keys['d'])

    def check_player2_getup_input(self):
        """Player2의 기상 입력 확인 (방향키 중 아무거나)"""
        return (self.player2_keys['up'] or self.player2_keys['down'] or
                self.player2_keys['left'] or self.player2_keys['right'])

    def checkEscape(self, events):
        """ESC 키로 종료 요청 감지"""
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    return True
        return False

import pico2d


class IOManager:
    def __init__(self):
        pass

    def handleInputPlayer1(self, events):  # events 매개변수 추가 (프레임마다 호출)
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_w:
                    return 'up'
                if event.key == pico2d.SDLK_s:
                    return 'down'
                if event.key == pico2d.SDLK_a:
                    return 'left'
                if event.key == pico2d.SDLK_d:
                    return 'right'
                return None  # 입력 없음

    def handleInputPlayer2(self, events):  # 동일하게 수정
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_UP:
                    return 'up'
                if event.key == pico2d.SDLK_DOWN:
                    return 'down'
                if event.key == pico2d.SDLK_LEFT:
                    return 'left'
                if event.key == pico2d.SDLK_RIGHT:
                    return 'right'
                return None

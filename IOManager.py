import pico2d


class IOManager:
    def __init__(self):
        self.Player1key = pico2d.get_events()
        self.Player2key = pico2d.get_events()
        pass

    def handleInputPlayer1(self):
        if self.Player1key == [pico2d.SDLK_w]:
            return 'up'
        if self.Player1key == [pico2d.SDLK_s]:
            return 'down'
        if self.Player1key == [pico2d.SDLK_a]:
            return 'left'
        if self.Player1key == [pico2d.SDLK_d]:
            return 'right'
        pass

    def handleInputPlayer2(self):
        if self.Player2key == [pico2d.SDLK_UP]:
            return 'up'
        if self.Player2key == [pico2d.SDLK_DOWN]:
            return 'down'
        if self.Player2key == [pico2d.SDLK_LEFT]:
            return 'left'
        if self.Player2key == [pico2d.SDLK_RIGHT]:
            return 'right'
        pass
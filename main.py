import game
import time
import pico2d

game = game.Game()
game.initialize()

def main():
    while game.running:
        game.run()

    pico2d.close_canvas()

if __name__ == "__main__":
    main()
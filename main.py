import Game  # 기존 그대로
# game을 글로벌로 선언 (while 루프 안에서 사용)

game = Game.Game()
game.initialize()

def main():

    while game.running:
        game.run()


if __name__ == "__main__":
    main()
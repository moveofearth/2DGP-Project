import Game

game = Game.Game()
game.initialize()

def main():


    while game.running:
        game.run()



if __name__ == "__main__":
    main()
"""{{ project_name }} project Main Game Loop"""

from xodex.game.game import Game


if __name__ == "__main__":
    game = Game("{{ project_name }}")
    game.main_loop()

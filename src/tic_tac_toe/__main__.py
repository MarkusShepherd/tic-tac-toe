import random

from tic_tac_toe.core import HumanPlayer, Player, TicTacToe


def main() -> None:
    players = [
        HumanPlayer("You"),
        Player("Random"),
    ]
    random.shuffle(players)
    game = TicTacToe(players=players)
    game.play()


if __name__ == "__main__":
    main()

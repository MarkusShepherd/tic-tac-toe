import random

from tic_tac_toe.core import HeuristicPlayer, HumanPlayer, TicTacToe


def main() -> None:
    players = [
        HumanPlayer("You"),
        HeuristicPlayer("Heuristic"),
    ]
    random.shuffle(players)
    game = TicTacToe(players=players, verbose=True)
    game.play()


if __name__ == "__main__":
    main()

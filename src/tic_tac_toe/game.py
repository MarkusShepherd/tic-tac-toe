from typing import Any

import numpy as np


class TicTacToe:
    def __init__(self) -> None:
        # Initialize an empty board
        self.board: np.ndarray[int, np.dtype[Any]] = np.zeros(
            (3, 3),
            dtype=int,
        )
        self.current_player: int = 1  # Player 1 starts the game
        self.winner: int | None = None
        self.game_over: bool = False

    def reset(self) -> None:
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.winner = None
        self.game_over = False

    def get_valid_moves(self) -> list[tuple[int, int]]:
        return list(
            # Get indices of empty cells
            zip(*np.where(self.board == 0), strict=False),
        )

    def is_valid_move(self, move: tuple[int, int]) -> bool:
        return bool(self.board[move[0], move[1]] == 0)  # Check if the cell is empty

    def make_move(self, move: tuple[int, int]) -> bool:
        if not self.is_valid_move(move) or self.game_over:
            return False

        self.board[move[0], move[1]] = self.current_player

        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif not self.get_valid_moves():
            self.game_over = True  # Draw

        self.current_player = 3 - self.current_player  # Switch players
        return True

    def check_winner(self) -> bool:
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if np.all(self.board[i, :] == self.current_player) or np.all(
                self.board[:, i] == self.current_player,
            ):
                return True
        if np.all(np.diag(self.board) == self.current_player) or np.all(
            np.diag(np.fliplr(self.board)) == self.current_player,
        ):
            return True
        return False

    def print_board(self) -> str:
        symbols = {0: "-", 1: "X", 2: "O"}
        result = ""
        for row in self.board:
            result += "|".join(symbols[cell] for cell in row) + "\n"
            result += "-" * 5 + "\n"
        return result


# Example usage:
if __name__ == "__main__":
    game = TicTacToe()
    while not game.game_over:
        print(game.print_board())
        valid_moves = game.get_valid_moves()
        move_str = input("Enter your move (row col): ")
        move = tuple(map(int, move_str.split()))
        if len(move) == 2 and move in valid_moves:
            game.make_move(move)
        else:
            pass
    print(game.print_board())
    if game.winner:
        pass
    else:
        pass

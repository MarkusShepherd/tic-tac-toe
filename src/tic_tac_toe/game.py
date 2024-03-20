from typing import Any

import numpy as np


class TicTacToe:
    symbols = ("-", "X", "O")

    def __init__(self) -> None:
        # Initialize an empty board
        self.board: np.ndarray[int, np.dtype[Any]] = np.zeros(
            (3, 3),
            dtype=int,
        )
        self.current_player: int = 1  # Player 1 starts the game
        self.winner: int | None = None
        self.game_over: bool = False
        self.symbols_to_int = {symbol: idx for idx, symbol in enumerate(self.symbols)}

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

    def __str__(self) -> str:
        rows = ["".join(self.symbols[cell] for cell in row) for row in self.board]
        return "\n".join(rows)

    def state_to_str(self) -> str:
        return str(self)

    def str_to_state(self, state: str) -> tuple[np.ndarray[int, np.dtype[Any]], int]:
        board = np.array(
            [[self.symbols_to_int[cell] for cell in row] for row in state.split("\n")],
            dtype=int,
        )
        current_player = 1 if state.count("X") <= state.count("O") else 2
        return board, current_player

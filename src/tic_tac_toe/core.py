from collections.abc import Iterable
from typing import Any, ClassVar

import numpy as np


class TicTacToe:
    symbols: tuple[str, str, str] = ("-", "X", "O")
    symbols_to_int: ClassVar[dict[str, int]] = {
        symbol: idx for idx, symbol in enumerate(symbols)
    }

    board: np.ndarray[int, np.dtype[Any]]
    current_player: int
    winner: int | None
    finished: bool

    def __init__(self, players: Iterable["Player"] | None = None) -> None:
        players = tuple(players) if players is not None else ()
        if len(players) > 2:
            raise ValueError("TicTacToe can only have 2 players.")
        while len(players) < 2:
            players += (Player(f"Player {len(players) + 1}"),)
        self.players = (Player("Dummy"), *players)

        # Initialize an empty board
        self.reset()

    def reset(self) -> None:
        for player in self.players:
            if player is not None:
                player.reset(self)
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.winner = None
        self.finished = False

    def get_valid_moves(self) -> list[tuple[int, int]]:
        return list(
            # Get indices of empty cells
            zip(*np.where(self.board == 0), strict=False),
        )

    def is_valid_move(self, move: tuple[int, int]) -> bool:
        return bool(self.board[*move] == 0)  # Check if the cell is empty

    def make_move(self, move: tuple[int, int]) -> bool:
        if not self.is_valid_move(move) or self.finished:
            return False

        self.board[*move] = self.current_player

        if self.check_winner():
            self.finished = True
            self.winner = self.current_player
        elif not self.get_valid_moves():
            self.finished = True  # Draw

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

    @classmethod
    def str_to_state(cls, state: str) -> tuple[np.ndarray[int, np.dtype[Any]], int]:
        board = np.array(
            [[cls.symbols_to_int[cell] for cell in row] for row in state.split("\n")],
            dtype=int,
        )
        current_player = 1 if np.sum(board == 1) <= np.sum(board == 2) else 2
        return board, current_player

    def state_to_int(self) -> int:
        # Every cell can be in one of three states,
        # so we can treat the board as a base-3 number
        return int("".join(map(str, self.board.flatten())), 3)

    @classmethod
    def int_to_state(cls, state_int: int) -> tuple[np.ndarray[int, np.dtype[Any]], int]:
        # Convert the base-3 number to a 3x3 array
        board = np.array(
            list(np.base_repr(state_int, base=3).zfill(9)),
            dtype=int,
        ).reshape(3, 3)
        current_player = 1 if np.sum(board == 1) <= np.sum(board == 2) else 2
        return board, current_player


class Player:
    name: str
    elo_rating: float

    game: TicTacToe

    def __init__(
        self,
        name: str,
        elo_rating: float | None = None,
        random_seed: int | None = None,
    ) -> None:
        self.name = name
        self.elo_rating = elo_rating or 1200
        self.rng = np.random.default_rng(random_seed)

    def __str__(self) -> str:
        return f"Player <{self.name}>"

    def reset(self, game: TicTacToe) -> None:
        """Reset the player."""
        self.game = game

    def action(self) -> tuple[int, int]:
        return self.rng.choice(self.game.get_valid_moves())  # type: ignore[no-any-return]

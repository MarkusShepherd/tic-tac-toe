import re
from collections import defaultdict
from collections.abc import Iterable
from typing import Any, ClassVar

import numpy as np
from tqdm import trange

Action = tuple[int, int]


class TicTacToe:
    symbols: tuple[str, str, str] = ("-", "X", "O")
    symbols_to_int: ClassVar[dict[str, int]] = {
        symbol: idx for idx, symbol in enumerate(symbols)
    }

    board: np.ndarray[int, np.dtype[Any]]
    current_player: int
    winner: int | None
    finished: bool

    def __init__(
        self,
        players: Iterable["Player"] | None = None,
        *,
        verbose: bool = False,
    ) -> None:
        players = tuple(players) if players is not None else ()
        if len(players) > 2:
            raise ValueError("TicTacToe can only have 2 players.")
        while len(players) < 2:
            players += (Player(f"Player {len(players) + 1}"),)
        assert len(players) == 2
        self.players = (Player("Dummy"), *players)
        self.verbose = verbose

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

    def get_valid_moves(self) -> list[Action]:
        return list(
            # Get indices of empty cells
            zip(*np.where(self.board == 0), strict=False),
        )

    def is_valid_move(self, move: Action) -> bool:
        return bool(self.board[move[0], move[1]] == 0)  # Check if the cell is empty

    def make_move(self, move: Action) -> bool:
        if not self.is_valid_move(move) or self.finished:
            return False

        self.board[move[0], move[1]] = self.current_player

        if self.check_winner():
            self.finished = True
            self.winner = self.current_player
        elif not self.get_valid_moves():
            self.finished = True  # Draw

        self.current_player = 3 - self.current_player  # Switch players
        return True

    def check_winner(self, *, player: int | None = None) -> bool:
        # Check rows, columns, and diagonals for a win
        player = player or self.current_player
        assert player in (1, 2)
        for i in range(3):
            if np.all(self.board[i, :] == player) or np.all(self.board[:, i] == player):
                return True
        if np.all(np.diag(self.board) == player) or np.all(
            np.diag(np.fliplr(self.board)) == player,
        ):
            return True
        return False

    def __str__(self) -> str:
        player_name = self.players[self.current_player].name
        player_symbol = self.symbols[self.current_player]
        return f"Current player: {player_name} ({player_symbol})\n{self.state_to_str()}"

    def state_to_str(self) -> str:
        rows = ["".join(self.symbols[cell] for cell in row) for row in self.board]
        return "\n".join(rows)

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

    def play(self) -> None:
        while not self.finished:
            if self.verbose:
                print(self)
            current_player = self.players[self.current_player]
            action = current_player.action()
            assert self.is_valid_move(action)
            self.make_move(action)

        for i, player in enumerate(self.players):
            if player is not None:
                player.end_game(
                    1 if i == self.winner else 0.5 if self.winner is None else 0,
                )

        if self.verbose:
            if self.winner:
                print(f"Player {self.winner} wins!")
            else:
                print("It's a draw!")
            print(self.state_to_str())


class Player:
    name: str
    elo_rating: float

    game: TicTacToe

    state_values: dict[str, float]
    state_counts: dict[str, int]
    state_buffer: list[str]

    def __init__(
        self,
        name: str,
        *,
        elo_rating: float | None = None,
        random_seed: int | None = None,
    ) -> None:
        self.name = name
        self.elo_rating = elo_rating or 1200
        self.rng = np.random.default_rng(random_seed)
        self.state_values = defaultdict(float)
        self.state_counts = defaultdict(int)
        self.state_buffer = []

    def __str__(self) -> str:
        return f"Player <{self.name}>"

    def reset(self, game: TicTacToe) -> None:
        """Reset the player."""
        self.game = game
        self.state_buffer = []

    def action(self) -> Action:
        """Select an action at random."""
        self.state_buffer.append(self.game.state_to_str())
        return tuple(self.rng.choice(self.game.get_valid_moves()))

    def end_game(self, reward: float) -> None:
        """Update the state values based on the game outcome."""
        for state in self.state_buffer:
            self.state_counts[state] += 1
            self.state_values[state] += (
                reward - self.state_values[state]
            ) / self.state_counts[state]


class HeuristicPlayer(Player):
    def __init__(
        self,
        name: str,
        *,
        epsilon: float | None = None,
        elo_rating: float | None = None,
        random_seed: int | None = None,
    ) -> None:
        super().__init__(name=name, elo_rating=elo_rating, random_seed=random_seed)
        self.epsilon = epsilon

    def _random_action(self) -> Action:
        return tuple(self.rng.choice(self.game.get_valid_moves()))

    def action(self) -> Action:
        self.state_buffer.append(self.game.state_to_str())

        # Epsilon exploration
        if self.epsilon and self.rng.random() < self.epsilon:
            return self._random_action()

        # Check if we can win in the next move
        valid_moves = self.game.get_valid_moves()
        self.rng.shuffle(valid_moves)
        for move in valid_moves:
            self.game.board[move] = self.game.current_player
            if self.game.check_winner(player=self.game.current_player):
                self.game.board[move] = 0
                return move
            self.game.board[move] = 0

        # Check if the opponent can win in the next move
        opponent = 3 - self.game.current_player
        valid_moves = self.game.get_valid_moves()
        self.rng.shuffle(valid_moves)
        for move in valid_moves:
            self.game.board[move] = opponent
            if self.game.check_winner(player=opponent):
                self.game.board[move] = 0
                return move
            self.game.board[move] = 0

        # Check if the center is empty
        if self.game.board[1, 1] == 0:
            return 1, 1

        # Check if a corner is empty
        corner_moves = [(0, 0), (0, 2), (2, 0), (2, 2)]
        self.rng.shuffle(corner_moves)
        for move in corner_moves:
            if self.game.board[move] == 0:
                return move

        # Select an empty cell at random
        return self._random_action()


class HumanPlayer(Player):
    match_regex = re.compile(r"\D*(\d)\D+(\d)")

    def action(self) -> Action:
        print(f"{self.game.get_valid_moves()}")
        response = input("Enter move (row, column): ")
        while True:
            match = self.match_regex.match(response)
            if match:
                move = tuple(map(int, match.groups()))
                assert len(move) == 2
                if self.game.is_valid_move(move):
                    return move
            response = input("Invalid move. Enter move (row, column): ")


def format_state_value(game: TicTacToe) -> str:
    players = game.players[1:]
    state = game.state_to_str()
    value = max(player.state_values[state] for player in players)
    return f"State:\n{state}\nValue: {value:.5f}"


def main(num_games: int = 10_000) -> None:
    player_1 = HeuristicPlayer("🤖1️⃣", epsilon=0.05)
    player_2 = HeuristicPlayer("🤖2️⃣", epsilon=0.05)
    game = TicTacToe(players=(player_1, player_2), verbose=False)
    print(f"Playing {num_games} games…")
    for _ in trange(num_games):
        game.play()
        game.reset()
    print(format_state_value(game))
    print()
    for x in range(3):
        for y in range(3):
            game.reset()
            game.board[x, y] = 1
            print(format_state_value(game))
            print()


if __name__ == "__main__":
    main()

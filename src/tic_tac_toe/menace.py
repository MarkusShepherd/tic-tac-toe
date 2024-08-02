"""
Implementation of the "Matchbox Educable Noughts and Crosses Engine" (MENACE) for
Tic-Tac-Toe.
"""

from collections import Counter

import numpy as np
from tqdm import trange

from tic_tac_toe.core import Action, HumanPlayer, Player, TicTacToe, format_state_value
from tic_tac_toe.exceptions import PlayerResignedError


class MENACE(Player):
    """Matchbox Educable Noughts and
    Crosses Engine (MENACE) for Tic-Tac-Toe."""

    def __init__(
        self,
        name: str,
        *,
        infinite_exploration: bool = False,
        elo_rating: float | None = None,
        random_seed: int | None = None,
    ) -> None:
        super().__init__(
            name=name,
            elo_rating=elo_rating,
            random_seed=random_seed,
        )
        self.infinite_exploration = infinite_exploration
        self.action_buffer: dict[str, Action] = {}
        self.matchboxes = self._seed_matchboxes()

    def _seed_matchboxes(self) -> dict[str, Counter[Action]]:
        """Seed the matchboxes with all possible states and moves."""
        matchboxes = {}
        game = TicTacToe()
        for i in range(3**9):
            state, _ = game.int_to_state(i)
            game.board = state
            beads = (state == 0).sum() // 2
            if not beads:
                continue
            matchbox = Counter({move: beads for move in game.get_valid_moves()})
            matchboxes[game.state_to_str()] = matchbox
        return matchboxes

    def reset(self, game: TicTacToe) -> None:
        """Reset the player for a new game."""
        super().reset(game)
        self.action_buffer = {}

    def action(self) -> Action:
        state = self.game.state_to_str()
        self.state_buffer.append(state)
        valid_moves = self.game.get_valid_moves()
        if len(valid_moves) == 1:
            return valid_moves[0]
        matchbox = self.matchboxes[state]
        total = matchbox.total()
        if total < 1:
            raise PlayerResignedError
        probs = np.array([matchbox[move] for move in valid_moves]) / total
        action = tuple(self.rng.choice(valid_moves, p=probs))
        self.action_buffer[state] = action
        return action

    def end_game(self, reward: float) -> None:
        super().end_game(reward)
        add_beads = 3 if reward == 1 else -1 if reward == 0 else 1
        for state, action in self.action_buffer.items():
            matchbox = self.matchboxes[state]
            matchbox[action] += add_beads
            if matchbox[action] < 0:
                matchbox[action] = 0
            if self.infinite_exploration:
                matchbox | {move: 1 for move in self.game.get_valid_moves()}

    def format_matchbox(self, state_str: str) -> str:
        state, _ = TicTacToe.str_to_state(state_str)
        matchbox = self.matchboxes[state_str]
        probs = np.zeros((3, 3))
        total = matchbox.total()
        for action, count in matchbox.items():
            probs[action] = count / total if total else 0
        result = "+" + ("-" * 24) + "+\n"
        for state_row, prob_row in zip(state, probs, strict=False):
            result += "| "
            for cell, prob in zip(state_row, prob_row, strict=False):
                if cell:
                    cell_str = TicTacToe.symbols[cell].center(5)
                else:
                    cell_str = f"{prob:5.1%}"
                    if len(cell_str) > 5:
                        cell_str = " 100%"
                result += f" {cell_str} |"
            result += "\n"
        result += "+" + ("-" * 24) + "+"
        return result


def main(num_games: int = 10_000) -> None:
    menace1 = MENACE("MENACE 1", infinite_exploration=True)
    menace2 = MENACE("MENACE 2", infinite_exploration=True)
    players: list[Player] = [menace1, menace2]
    game = TicTacToe(players=players, verbose=False)
    print(f"Playing {num_games} games…")
    for _ in trange(num_games):
        game.play()
        game.reset()

    first_state = game.state_to_str()
    print(format_state_value(game))
    print(menace1.format_matchbox(first_state))
    print()

    for x in range(3):
        for y in range(3):
            game.reset()
            game.board[x, y] = 1
            print(format_state_value(game))
            print(menace2.format_matchbox(game.state_to_str()))
            print()

    players = [menace1, HumanPlayer("You")]
    game = TicTacToe(players=players, verbose=True)
    game.play()


if __name__ == "__main__":
    main(num_games=100_000)

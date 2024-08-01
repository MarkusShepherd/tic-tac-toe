"""
Implementation of the "Matchbox Educable Noughts and Crosses Engine" (MENACE) for
Tic-Tac-Toe.
"""

from collections import Counter

from tic_tac_toe.core import Action, Player, TicTacToe


class MENACE(Player):
    """Matchbox Educable Noughts and
    Crosses Engine (MENACE) for Tic-Tac-Toe."""

    def __init__(
        self,
        name: str,
        *,
        elo_rating: float | None = None,
        random_seed: int | None = None,
    ) -> None:
        super().__init__(name=name, elo_rating=elo_rating, random_seed=random_seed)
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
        matchbox = self.matchboxes[state]
        actions = list(matchbox.elements())
        if not actions:
            # TODO(Markus): Gracefully resign the game
            raise ValueError(f"No valid moves for state {state}")
        action = tuple(self.rng.choice(actions))
        self.action_buffer[state] = action
        return action

    def end_game(self, reward: float) -> None:
        super().end_game(reward)
        add_beads = 3 if reward == 1 else -1 if reward == 0 else 1
        for state in self.state_buffer:
            matchbox = self.matchboxes[state]
            action = self.action_buffer[state]
            matchbox[action] += add_beads

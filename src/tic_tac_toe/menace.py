"""
Implementation of the "Matchbox Educable Noughts and Crosses Engine" (MENACE) for
Tic-Tac-Toe.
"""

from collections import Counter

from tqdm import trange

from tic_tac_toe.core import Action, HumanPlayer, Player, TicTacToe, format_state_value


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
        valid_moves = self.game.get_valid_moves()
        if len(valid_moves) == 1:
            return valid_moves[0]
        matchbox = self.matchboxes[state]
        actions = list(matchbox.elements())
        # TODO(Markus): Original MENACE would resign if the matchbox is empty
        action = tuple(self.rng.choice(actions or valid_moves))
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


def main(num_games: int = 10_000) -> None:
    menace1 = MENACE("MENACE 1")
    menace2 = MENACE("MENACE 2")
    players: list[Player] = [menace1, menace2]
    game = TicTacToe(players=players, verbose=False)
    print(f"Playing {num_games} games…")
    for _ in trange(num_games):
        game.play()
        game.reset()

    first_state = game.state_to_str()
    matchbox = menace1.matchboxes[first_state]
    print(f"Beads in first box: {matchbox.total()}")
    print(matchbox)
    print()

    print(format_state_value(game))
    print()

    for x in range(3):
        for y in range(3):
            game.reset()
            game.board[x, y] = 1
            print(format_state_value(game))
            print()

    players = [menace1, HumanPlayer("You")]
    game = TicTacToe(players=players, verbose=True)
    game.play()


if __name__ == "__main__":
    main()

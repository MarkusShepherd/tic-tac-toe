import unittest

from tic_tac_toe.game import TicTacToe


class TicTacToeTests(unittest.TestCase):
    def test_initial_state(self) -> None:
        game = TicTacToe()
        assert game.board.tolist() == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert game.current_player == 1
        assert game.winner is None
        assert not game.game_over

    def test_reset(self) -> None:
        game = TicTacToe()
        game.board[0, 0] = 1
        game.current_player = 2
        game.winner = 1
        game.game_over = True

        game.reset()

        assert game.board.tolist() == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert game.current_player == 1
        assert game.winner is None
        assert not game.game_over

    def test_get_valid_moves(self) -> None:
        game = TicTacToe()
        game.board[0, 0] = 1
        game.board[1, 1] = 2
        game.board[2, 2] = 1

        valid_moves = game.get_valid_moves()

        assert valid_moves == [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

    def test_is_valid_move(self) -> None:
        game = TicTacToe()
        game.board[0, 0] = 1
        game.board[1, 1] = 2

        assert game.is_valid_move((0, 1))
        assert not game.is_valid_move((0, 0))
        assert not game.is_valid_move((1, 1))

    def test_make_move(self) -> None:
        game = TicTacToe()
        game.make_move((0, 0))
        game.make_move((1, 1))
        game.make_move((0, 1))
        game.make_move((1, 0))
        game.make_move((0, 2))

        assert game.board.tolist() == [[1, 1, 1], [2, 2, 0], [0, 0, 0]]
        assert game.current_player == 2
        assert game.winner == 1
        assert game.game_over

    def test_check_winner(self) -> None:
        game = TicTacToe()
        game.current_player = 1
        game.board[0, 0] = 1
        game.board[0, 1] = 1
        game.board[0, 2] = 1

        assert game.check_winner()

        game.reset()

        game.current_player = 2
        game.board[1, 0] = 2
        game.board[1, 1] = 2
        game.board[1, 2] = 2

        assert game.check_winner()

        game.reset()

        game.current_player = 1
        game.board[2, 0] = 1
        game.board[1, 1] = 1
        game.board[0, 2] = 1

        assert game.check_winner()

        game.reset()

        game.current_player = 2
        game.board[0, 0] = 2
        game.board[1, 1] = 2
        game.board[2, 2] = 2

        assert game.check_winner()

        game.reset()

        game.board[0, 0] = 1
        game.board[1, 1] = 2
        game.board[2, 2] = 1

        assert not game.check_winner()

    def test_board_str(self) -> None:
        game = TicTacToe()
        game.board[0, 0] = 1
        game.board[1, 1] = 2
        game.board[2, 2] = 1

        expected_output = "X|-|-\n-----\n-|O|-\n-----\n-|-|X\n-----\n"

        assert str(game) == expected_output

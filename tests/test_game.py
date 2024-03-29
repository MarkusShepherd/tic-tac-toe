import unittest

import numpy as np
from tic_tac_toe.core import TicTacToe


class TicTacToeTests(unittest.TestCase):
    state_str = "X--\n-O-\n--X"
    board = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 1]], dtype=int)

    def test_initial_state(self) -> None:
        game = TicTacToe()
        assert game.board.tolist() == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert game.current_player == 1
        assert game.winner is None
        assert not game.finished

    def test_reset(self) -> None:
        game = TicTacToe()
        game.board[0, 0] = 1
        game.current_player = 2
        game.winner = 1
        game.finished = True

        game.reset()

        assert game.board.tolist() == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert game.current_player == 1
        assert game.winner is None
        assert not game.finished

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
        assert game.finished

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
        game.board = self.board
        expected_str = f"Current player: Player 1 (X)\n{self.state_str}"
        assert str(game) == expected_str

    def test_state_to_str(self) -> None:
        game = TicTacToe()
        game.board = self.board
        assert game.state_to_str() == self.state_str

    def test_str_to_state(self) -> None:
        expected_current_player = 2
        board, current_player = TicTacToe.str_to_state(self.state_str)
        assert np.array_equal(board, self.board)
        assert current_player == expected_current_player

    def test_state_to_int(self) -> None:
        game = TicTacToe()
        game.board = self.board
        expected_result = int("100020001", 3)
        result = game.state_to_int()
        assert result == expected_result

    def test_int_to_state(self) -> None:
        state_int = int("100020001", 3)
        expected_current_player = 2
        board, current_player = TicTacToe.int_to_state(state_int)
        assert np.array_equal(board, self.board)
        assert current_player == expected_current_player

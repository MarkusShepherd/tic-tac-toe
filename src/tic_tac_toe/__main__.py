from tic_tac_toe.game import TicTacToe


def main() -> None:
    game = TicTacToe()
    while not game.game_over:
        print(game.print_board())
        valid_moves = game.get_valid_moves()
        print("Valid moves:", valid_moves)
        move_str = input("Enter your move (row col): ")
        move = tuple(map(int, move_str.split()))
        if len(move) == 2 and move in valid_moves:
            game.make_move(move)
        else:
            print("Invalid move. Try again.")
    print(game.print_board())
    if game.winner:
        print("Player", game.winner, "wins!")
    else:
        print("It's a draw!")


# Example usage:
if __name__ == "__main__":
    main()

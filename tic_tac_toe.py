"""Two-player console tic-tac-toe. Positions are numbered 1-9."""

WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
             (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
             (0, 4, 8), (2, 4, 6)]              # diagonals

def show(board):
    print(f"\n{board[0]} | {board[1]} | {board[2]}\n--+---+--\n"
          f"{board[3]} | {board[4]} | {board[5]}\n--+---+--\n"
          f"{board[6]} | {board[7]} | {board[8]}\n")

board = [str(i) for i in range(1, 10)]  # free cells display their position number
player = "X"

show(board)
for _ in range(9):
    while True:
        pos = input(f"Player {player}, pick a position (1-9): ").strip()
        if pos.isdigit() and 1 <= int(pos) <= 9 and board[int(pos) - 1] not in ("X", "O"):
            break
        print("Invalid choice, try again.")
    board[int(pos) - 1] = player
    show(board)
    if any(board[a] == board[b] == board[c] for a, b, c in WIN_LINES):
        print(f"Player {player} wins!")
        break
    player = "O" if player == "X" else "X"
else:
    print("It's a draw!")

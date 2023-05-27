import random
from typing import List, Tuple
from minimax import minimax
from tqdm import tqdm


# Function to print the Tic-Tac-Toe board
def print_board(board: List[List[str]]) -> None:
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


# Function to check if the game is over
def is_game_over(board: List[List[str]]) -> bool:
    # Check rows
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != " ":
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True

    # Check for tie
    if all(board[i][j] != " " for i in range(3) for j in range(3)):
        return True

    return False


# Function to evaluate the board heuristic
def evaluate_board(board: List[List[str]]) -> float:
    # Heuristic value for each possible outcome
    if is_winner(board, "X"):
        return 1.0  # You win
    elif is_winner(board, "O"):
        return -1.0  # Opponent wins
    else:
        return 0.0  # It's a tie


# Function to get all possible moves
def get_possible_moves(board: List[List[str]]) -> List[Tuple[int, int]]:
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves


# Function to make a move
def make_move(
    board: List[List[str]], move: Tuple[int, int], is_maximizing: bool
) -> List[List[str]]:
    new_board = [row[:] for row in board]
    new_board[move[0]][move[1]] = "X" if is_maximizing else "O"
    return new_board


# Function to check if a player has won
def is_winner(board: List[List[str]], player: str) -> bool:
    # Check rows
    for row in board:
        if row.count(player) == len(row):
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False


def test_minimax() -> None:
    wins = 0
    losses = 0
    ties = 0

    for _ in tqdm(range(100)):
        board = [[" ", " ", " "] for _ in range(3)]
        player = "X"

        while not is_game_over(board):
            print(board)
            if player == "X":
                # Your turn
                _, move = minimax(
                    board,
                    get_possible_moves,
                    make_move,
                    is_game_over,
                    evaluate_board,
                    9,
                    True,
                )
                board = make_move(board, move, True)
                player = "O"
            else:
                # Random opponent's turn
                moves = get_possible_moves(board)
                move = random.choice(moves)
                board = make_move(board, move, False)
                player = "X"

        if is_winner(board, "X"):
            wins += 1
        elif is_winner(board, "O"):
            losses += 1
        else:
            ties += 1

    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Ties: {ties}")


# Test the minimax strategy
if __name__ == "__main__":
    test_minimax()

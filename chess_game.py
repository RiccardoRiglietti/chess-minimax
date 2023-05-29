import chess
from typing import List
import random
from minimax import minimax
from tqdm import tqdm

def get_possible_moves(state: chess.Board) -> List[chess.Move]:
    return list(state.legal_moves)


def make_move(
    state: chess.Board, move: chess.Move, is_maximizing_player: bool
) -> None:
    #new_state = state.copy()
    state.push(move)
    return None
    #return new_state

def undo_move(state: chess.Board, move: chess.Move, is_maximizing_player: bool) -> None:
    state.pop()
    
def is_game_over(state: chess.Board) -> bool:
    return state.is_game_over()

#@cached
def evaluate_board(state: chess.Board) -> float:
    # Check if the game is over
    if state.is_game_over():
        result = state.result()
        if result == '1-0':  # White wins
            return 1000.0
        elif result == '0-1':  # Black wins
            return -1000.0
        elif result == '1/2-1/2':  # Draw
            return 0.0

    # Evaluation for the ongoing game
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }

    score = 0.0
    for square in chess.SQUARES:
        piece = state.piece_at(square)
        if piece is not None:
            value = piece_values.get(piece.piece_type, 0)
            if piece.color == chess.WHITE:
                score += value
                # Bonus for pieces in the center
                if square in [24, 40]:
                    score += 0.001
                # Bonus for pushing pawns forward
                if piece.piece_type == chess.PAWN:
                    rank = chess.square_rank(square)
                    if piece.color == chess.WHITE:
                        score += 0.001 * rank
                    else:
                        score += 0.001 * (7 - rank)
            else:
                score -= value
                # Bonus for pieces in the center
                if square in [24, 40]:
                    score -= 0.001
                # Bonus for pushing pawns forward
                if piece.piece_type == chess.PAWN:
                    rank = chess.square_rank(square)
                    if piece.color == chess.WHITE:
                        score -= 0.001 * (7 - rank)
                    else:
                        score -= 0.001 * rank

    return score


# Function to simulate a random opponent move
def random_opponent_move(state: chess.Board) -> chess.Move:
    legal_moves = list(state.legal_moves)
    return random.choice(legal_moves)


# Function to play a single game
def play_game_random_opponent(depth) -> float:
    state = chess.Board()
    is_maximizing_player = True
    while not state.is_game_over():
        if is_maximizing_player:
            eval, move = minimax(
                state,
                get_possible_moves,
                make_move,
                undo_move,
                is_game_over,
                evaluate_board,
                depth=depth,
                is_maximizing_player=True,
            )
            #display_board(state)
            #print(eval)
        else:
            move = random_opponent_move(state)
        state.push(move)
        is_maximizing_player = not is_maximizing_player

    result = state.result()
    #print(result)
    #print("Final board:")
    #display_board(state)
    if result == "1-0":
        return 1.0  # AI wins
    elif result == "0-1":
        return -1.0  # Random opponent wins
    else:
        return 0.0  # Draw

def test_against_random(N, depth=2):
    # Run 100 games
    ai_wins = 0
    opponent_wins = 0
    draws = 0
    for _ in tqdm(range(N)):
        result = play_game_random_opponent(depth)
        if result == 1.0:
            ai_wins += 1
        elif result == -1.0:
            opponent_wins += 1
        else:
            draws += 1

    # Print the results
    print("AI wins:", ai_wins)
    print("Opponent wins:", opponent_wins)
    print("Draws:", draws)


# Function to display the chessboard with Unicode piece representation
def display_board(state: chess.Board) -> None:
    piece_symbols = {
        chess.PAWN: "♙ ♟",
        chess.KNIGHT: "♘ ♞",
        chess.BISHOP: "♗ ♝",
        chess.ROOK: "♖ ♜",
        chess.QUEEN: "♕ ♛",
        chess.KING: "♔ ♚",
    }

    print("  a b c d e f g h")
    for rank in range(8, 0, -1):
        row = str(rank) + " "
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = state.piece_at(square)
            if piece is None:
                row += "·"
            else:
                symbol = piece_symbols[piece.piece_type]
                if piece.color == chess.WHITE:
                    row += symbol[0]
                else:
                    row += symbol[2]
            row += " "
        print(row)
    print("  a b c d e f g h")

# Function to convert user-friendly input to a move
def parse_user_input(move_str: str) -> chess.Move:
    file_from = ord(move_str[0]) - ord('a')
    rank_from = int(move_str[1]) - 1
    square_from = chess.square(file_from, rank_from)
    file_to = ord(move_str[2]) - ord('a')
    rank_to = int(move_str[3]) - 1
    square_to = chess.square(file_to, rank_to)
    return chess.Move(square_from, square_to)

# Function to play a single game against a human player
def play_game(depth) -> float:
    state = chess.Board()
    is_human_turn = True
    while not state.is_game_over():
        if is_human_turn:
            display_board(state)
            user_move_str = input("Enter your move (e.g., 'e2e4'): ")
            user_move = parse_user_input(user_move_str)
            while user_move not in state.legal_moves:
                print("Invalid move. Please try again.")
                user_move_str = input("Enter your move (e.g., 'e2e4'): ")
                user_move = parse_user_input(user_move_str)
            move = user_move
        else:
            move = minimax(state, get_possible_moves, make_move, undo_move, is_game_over, evaluate_board, depth=depth, is_maximizing_player=False)[1]
        state.push(move)
        is_human_turn = not is_human_turn

    result = state.result()
    if result == '1-0':
        return 1.0  # AI wins
    elif result == '0-1':
        return -1.0  # Human player wins
    else:
        return 0.0  # Draw

if __name__ == "__main__":
    test_against_random(50, depth=2)
    result = play_game(depth=4)
    if result == 1.0:
        print("AI wins!")
    elif result == -1.0:
        print("Human player wins!")
    else:
        print("Draw!")

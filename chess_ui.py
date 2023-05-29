import chess
import tkinter as tk
from PIL import ImageTk, Image
from functools import partial
from minimax import minimax
import chess_game
import time
from playsound import playsound

# Constants
BOARD_SIZE = 800
SQUARE_SIZE = BOARD_SIZE // 8

# Create the chessboard GUI
class ChessUI(tk.Tk):
    def __init__(self, depth=3):
        super().__init__()
        self.depth = depth
        self.title("Chess Game")
        self.geometry(f"{BOARD_SIZE}x{BOARD_SIZE}")

        # Create the chessboard canvas
        self.canvas = tk.Canvas(self, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack(side=tk.LEFT)

        # Load chess piece images
        self.piece_images = {
            chess.PAWN: {
                chess.WHITE: self.load_image("images/pawn_white.png"),
                chess.BLACK: self.load_image("images/pawn_black.png"),
            },
            chess.KNIGHT: {
                chess.WHITE: self.load_image("images/knight_white.png"),
                chess.BLACK: self.load_image("images/knight_black.png"),
            },
            chess.BISHOP: {
                chess.WHITE: self.load_image("images/bishop_white.png"),
                chess.BLACK: self.load_image("images/bishop_black.png"),
            },
            chess.ROOK: {
                chess.WHITE: self.load_image("images/rook_white.png"),
                chess.BLACK: self.load_image("images/rook_black.png"),
            },
            chess.QUEEN: {
                chess.WHITE: self.load_image("images/queen_white.png"),
                chess.BLACK: self.load_image("images/queen_black.png"),
            },
            chess.KING: {
                chess.WHITE: self.load_image("images/king_white.png"),
                chess.BLACK: self.load_image("images/king_black.png"),
            },
        }

        # Initialize the chessboard
        self.board = chess.Board()
        self.selected_piece = None
        self.evaluation = 0.5

        # Draw the initial chessboard
        self.draw_board()

        # Bind the click event to handle moves
        self.canvas.bind("<Button-1>", self.handle_click)
        

    def load_image(self, path):
        image = Image.open(path)
        image = image.resize((SQUARE_SIZE, SQUARE_SIZE), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

    def draw_board(self):
        self.canvas.delete("all")
        for rank in range(8):
            for file in range(8):
                x1 = file * SQUARE_SIZE
                y1 = rank * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                color = "#FFFACD" if (rank + file) % 2 == 0 else "#7D946C"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                square = chess.square(file, 7 - rank)
                piece = self.board.piece_at(square)
                if piece:
                    image = self.piece_images[piece.piece_type][piece.color]
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=image)
                #print(f"Chosen piece square {self.selected_piece}, check with {square}")
                if self.selected_piece == square:
                    print("MATCH", self.selected_piece, square)
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=4)
                    moves = self.board.legal_moves
                    for move in moves:
                        if move.from_square == self.selected_piece:
                            print(f"FROM possibility {move.from_square}, selected {self.selected_piece}")
                            target_square = move.to_square
                            target_rank = 7 - chess.square_rank(target_square)
                            target_file = chess.square_file(target_square)
                            target_x1 = target_file * SQUARE_SIZE
                            target_y1 = target_rank * SQUARE_SIZE
                            target_x2 = target_x1 + SQUARE_SIZE
                            target_y2 = target_y1 + SQUARE_SIZE
                            self.canvas.create_rectangle(target_x1, target_y1, target_x2, target_y2, outline="yellow", width=4)

        if self.board.is_game_over():
            print("Game over")
            return

    def handle_click(self, event):
        rank = event.y // SQUARE_SIZE
        file = event.x // SQUARE_SIZE
        square = chess.square(file, 7 - rank)
        print(self.board.legal_moves)
        if self.selected_piece is None:
            piece = self.board.piece_at(square)
            if piece.color == self.board.turn:
                self.selected_piece = square
                print("selecting", square)
        else:
            if self.selected_piece == square:
                self.selected_piece = None
                print("deselecting")
            else:
                print("try making move")
                move = chess.Move(self.selected_piece, square)
                #print(move, list(self.board.legal_moves))
                if move in self.board.legal_moves:
                    self.board.push(move)
                    playsound("sounds/move_sound.wav", block=False)
                    self.selected_piece = None
                else:
                    self.selected_piece = square
        
        print("Drawing board")
        print(self.board)
        self.draw_board()
        self.update()
        print("Making cpu move")
        self.make_cpu_move()  # Call CPU move after the human player's move
        print("Drawing board 2")
        self.draw_board()

    def make_cpu_move(self):
        if not self.board.is_game_over() and not self.board.turn:
            # CPU's turn, make a move using minimax algorithm
            self.evaluation, move = minimax(
                self.board,
                chess_game.get_possible_moves,
                chess_game.make_move,
                chess_game.is_game_over,
                chess_game.evaluate_board,
                depth=self.depth,
                is_maximizing_player=False,
            )
            self.board.push(move)
            playsound("sounds/move_sound.wav", block=False)

# Start the chess game
if __name__ == "__main__":
    ChessUI(depth=4).mainloop()

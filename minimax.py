from typing import Any, Callable, List, Tuple, TypeVar
from cachetools import cached
from cachetools.keys import hashkey

State = TypeVar("State")
Move = TypeVar("Move")

def key_hash(    state: Any,
    get_possible_moves: Callable[[State], List[Move]],
    make_move: Callable[[State, Move, bool], State],
    is_game_over: Callable[[State], bool],
    evaluate_board: Callable[[State], float],
    depth: int,
    is_maximizing_player: bool,
    alpha: float = float("-inf"),
    beta: float = float("inf") ):
    return hashkey(str(state)+str(alpha)+str(beta))
@cached(    cache={},    key=key_hash)
def minimax(
    state: Any,
    get_possible_moves: Callable[[State], List[Move]],
    make_move: Callable[[State, Move, bool], State],
    is_game_over: Callable[[State], bool],
    evaluate_board: Callable[[State], float],
    depth: int,
    is_maximizing_player: bool,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> Tuple[float, Any]:
    if depth == 0 or is_game_over(state):
        return evaluate_board(state), None

    if is_maximizing_player:
        max_eval = float("-inf")
        best_move = None
        for move in get_possible_moves(state):
            new_state = make_move(state, move, is_maximizing_player)
            evaluation, _ = minimax(
                new_state,
                get_possible_moves,
                make_move,
                is_game_over,
                evaluate_board,
                depth - 1,
                False,
                alpha,
                beta,
            )
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, max_eval)
            if alpha > beta:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for move in get_possible_moves(state):
            new_state = make_move(state, move, is_maximizing_player)
            evaluation, _ = minimax(
                new_state,
                get_possible_moves,
                make_move,
                is_game_over,
                evaluate_board,
                depth - 1,
                True,
                alpha,
                beta,
            )
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, min_eval)
            if alpha > beta:
                break
        return min_eval, best_move

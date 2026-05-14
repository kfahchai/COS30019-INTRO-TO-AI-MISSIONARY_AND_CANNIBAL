'''game_logic.py
Missionaries and Cannibals core logic module.
Provides state handling, move validation, win/loss detection, and an
automatic BFS solver. The GUI in `standalone_game.py` can import and use
these functions to keep UI separate from game rules.
'''

from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# State representation
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class State:
    """Immutable representation of a game configuration.

    Attributes
    ----------
    missionaries_left: int
        Number of missionaries on the left bank.
    cannibals_left: int
        Number of cannibals on the left bank.
    missionaries_right: int
        Number of missionaries on the right bank.
    cannibals_right: int
        Number of cannibals on the right bank.
    boat_side: str
        Either "left" or "right" indicating where the boat currently is.
    """

    missionaries_left: int
    cannibals_left: int
    missionaries_right: int
    cannibals_right: int
    boat_side: str  # "left" or "right"

    def __post_init__(self) -> None:
        if self.boat_side not in {"left", "right"}:
            raise ValueError("boat_side must be 'left' or 'right'")

    def is_goal(self) -> bool:
        """Return True when all missionaries and cannibals are on the left side."""
        return (
            self.missionaries_left == 3 and
            self.cannibals_left == 3 and
            self.missionaries_right == 0 and
            self.cannibals_right == 0
        )

    def is_loss(self) -> bool:
        """Return True if missionaries are outnumbered on either bank.

        The rule only applies when missionaries are present on a bank.
        """
        left_bad = (
            self.missionaries_left != 0 and self.missionaries_left < self.cannibals_left
        )
        right_bad = (
            self.missionaries_right != 0 and self.missionaries_right < self.cannibals_right
        )
        return left_bad or right_bad

    def is_valid(self) -> bool:
        """Check that the state respects the problem constraints.

        - No negative counts.
        - No side has missionaries outnumbered by cannibals.
        """
        if any(x < 0 for x in (
            self.missionaries_left,
            self.cannibals_left,
            self.missionaries_right,
            self.cannibals_right,
        )):
            return False
        return not self.is_loss()

# ---------------------------------------------------------------------------
# Helper functions for state transitions
# ---------------------------------------------------------------------------
# Boat capacity is 2 and at least 1 person must travel.
_MOVE_OPTIONS: List[Tuple[int, int]] = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

def _apply_move(state: State, m: int, c: int) -> Optional[State]:
    """Return a new State after moving *m* missionaries and *c* cannibals.

    The move is applied in the direction opposite to ``state.boat_side`` –
    i.e. the boat travels from its current side to the other side.
    If the move would violate any rule, ``None`` is returned.
    """
    # Determine source and destination based on boat location.
    if state.boat_side == "right":
        # moving from right to left
        if m > state.missionaries_right or c > state.cannibals_right:
            return None
        new_state = State(
            missionaries_left=state.missionaries_left + m,
            cannibals_left=state.cannibals_left + c,
            missionaries_right=state.missionaries_right - m,
            cannibals_right=state.cannibals_right - c,
            boat_side="left",
        )
    else:  # boat on left
        if m > state.missionaries_left or c > state.cannibals_left:
            return None
        new_state = State(
            missionaries_left=state.missionaries_left - m,
            cannibals_left=state.cannibals_left - c,
            missionaries_right=state.missionaries_right + m,
            cannibals_right=state.cannibals_right + c,
            boat_side="right",
        )
    return new_state if new_state.is_valid() else None

def get_successors(state: State) -> List[Tuple[State, Tuple[int, int]]]:
    """Generate all reachable valid states from *state*.

    Returns a list of tuples ``(next_state, (m, c))`` where ``(m, c)``
    indicates the number of missionaries and cannibals moved in that step.
    """
    successors: List[Tuple[State, Tuple[int, int]]] = []
    for m, c in _MOVE_OPTIONS:
        nxt = _apply_move(state, m, c)
        if nxt is not None:
            successors.append((nxt, (m, c)))
    return successors

# ---------------------------------------------------------------------------
# BFS solver
# ---------------------------------------------------------------------------
def bfs_solve(initial: State | None = None) -> Optional[List[Tuple[int, int, str]]]:
    """Return the shortest sequence of moves that solves the puzzle.

    The result is a list of ``(missionaries, cannibals, direction)`` where
    ``direction`` is ``"left"`` when the boat ends on the left bank after the
    move and ``"right"`` otherwise. ``None`` is returned if the puzzle is
    unsolvable from the given *initial* state (which should never happen for
    the classic configuration).
    """
    if initial is None:
        # Default starting configuration: all people on the right, boat on the right.
        initial = State(0, 0, 3, 3, "right")

    queue: deque[Tuple[State, List[Tuple[int, int, str]]]] = deque()
    visited: set[State] = set()
    queue.append((initial, []))

    while queue:
        cur_state, path = queue.popleft()
        if cur_state in visited:
            continue
        visited.add(cur_state)

        if cur_state.is_goal():
            return path

        for nxt_state, (m, c) in get_successors(cur_state):
            if nxt_state in visited:
                continue
            # Record direction based on where the boat ends up.
            direction = nxt_state.boat_side
            queue.append((nxt_state, path + [(m, c, direction)]))

    return None

# ---------------------------------------------------------------------------
# Convenience helper used by the original UI script
# ---------------------------------------------------------------------------
def default_initial_state() -> State:
    """Factory for the classic starting state used by the UI script."""
    return State(0, 0, 3, 3, "right")

# The module is intentionally lightweight – it contains no I/O or UI code.
# UI scripts should import ``State`` and the functions above to manipulate
# the puzzle.

"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    target_colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob counted by unit
    cells of this goal's target colour, anywhere within the Block.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    target_colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize BlobGoal to have the given target colour.
        """
        super().__init__(target_colour)
        # subclass of goal, shouldn't need any new attributes

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        # implemented flatten but used list comprehensions
        flatten_board = board.flatten()
        # visited_lst creates a list of unvisited columns and rows given flatten
        visited_lst = [[-1] * len(flatten_board) for _ in range(
            len(flatten_board))]
        # used the helper to return ints and just took the max in the list
        # comprehension
        return max([self._undiscovered_blob_size((c, r), flatten_board,
                                                 visited_lst)
                    for c in range(len(flatten_board)) for r in
                    range(len(flatten_board))])

    def description(self) -> str:
        """Return a description of this goal.
        """
        # simple description to fit the screen
        return 'Create the largest connected blob of this colour'

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # checking whether or not the unit cell exists
        if not (0 <= pos[0] < len(board)) or not 0 <= pos[1] < len(board):
            return 0
        else:
            # using counters to keep track of the neighbour flattened blocks
            counter = 0
            if board[pos[0]][pos[1]] == self.colour and \
                    visited[pos[0]][pos[1]] == -1:
                visited[pos[0]][pos[1]] = 1
                counter += 1
                counter += self._undiscovered_blob_size(
                    (pos[0] + 1, pos[1]), board,
                    visited)
                counter += self._undiscovered_blob_size(
                    (pos[0] - 1, pos[1]), board,
                    visited)
                counter += self._undiscovered_blob_size(
                    (pos[0], pos[1] + 1), board,
                    visited)
                counter += self._undiscovered_blob_size(
                    (pos[0], pos[1] - 1), board,
                    visited)

            return counter


class PerimeterGoal(Goal):
    """ A goal to create units of this goal's target
    colour, anywhere within the Block that can cover the
    edges of the board.
    """

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize the PerimeterGoal to have the given target colour.
        """
        super().__init__(target_colour)

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        # use flatten to index at the top row, bottom row, left most column,
        # right most column
        flat_board = board.flatten()
        score = 0
        for i in range(len(flat_board)):
            if flat_board[i][0] == self.colour:
                score += 1
            if flat_board[i][-1] == self.colour:
                score += 1
            if flat_board[0][i] == self.colour:
                score += 1
            if flat_board[-1][i] == self.colour:
                score += 1
        return score

    def description(self) -> str:
        """Return a description of this goal.
        """
        # simple description to fit the screen
        return 'Try to get this colour on the edges of the screen'

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })

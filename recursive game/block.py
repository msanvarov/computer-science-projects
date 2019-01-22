"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Block class, the main data structure used in the game.
"""
from typing import Optional, Tuple, List
import random
import math
from renderer import COLOUR_LIST, TEMPTING_TURQUOISE, BLACK, colour_name


HIGHLIGHT_COLOUR = TEMPTING_TURQUOISE
FRAME_COLOUR = BLACK


class Block:
    """A square block in the Blocky game.

    === Public Attributes ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
        Note that (0, 0) is the top left corner of the window.
    size:
        The height and width of this Block.  Since all blocks are square,
        we needn't represent height and width separately.
    colour:
        If this block is not subdivided, <colour> stores its colour.
        Otherwise, <colour> is None and this block's sublocks store their
        individual colours.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero.  If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    highlighted:
        True iff the user has selected this block for action.
    children:
        The blocks into which this block is subdivided.  The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.
    parent:
        The block that this block is directly within.

    === Representation Invariations ===
    - len(children) == 0 or len(children) == 4
    - If this Block has children,
        - their max_depth is the same as that of this Block,
        - their size is half that of this Block,
        - their level is one greater than that of this Block,
        - their position is determined by the position and size of this Block,
          as defined in the Assignment 2 handout, and
        - this Block's colour is None
    - If this Block has no children,
        - its colour is not None
    - level <= max_depth
    """
    position: Tuple[int, int]
    size: int
    colour: Optional[Tuple[int, int, int]]
    level: int
    max_depth: int
    highlighted: bool
    children: List['Block']
    parent: Optional['Block']

    def __init__(self, level: int,
                 colour: Optional[Tuple[int, int, int]] = None,
                 children: Optional[List['Block']] = None) -> None:
        """Initialize this Block to be an unhighlighted root block with
        no parent.

        If <children> is None, give this block no children.  Otherwise
        give it the provided children.  Use the provided level and colour,
        and set everything else (x and y coordinates, size,
        and max_depth) to 0.  (All attributes can be updated later, as
        appropriate.)
        """
        if children is None:
            self.children = []
        else:
            self.children = children
        # chose to mutate the self.parent for each child in the random_init
        self.parent = None
        self.colour = colour
        self.level = level
        self.position = (0, 0)
        self.size = 0
        self.max_depth = 0
        # max_depth is mutated in random_init also to prevent problems with
        # smash
        self.highlighted = False

    def rectangles_to_draw(self) -> List[Tuple[Tuple[int, int, int],
                                               Tuple[int, int],
                                               Tuple[int, int],
                                               int]]:
        """
        Return a list of tuples describing all of the rectangles to be drawn
        in order to render this Block.

        This includes (1) for every undivided Block:
            - one rectangle in the Block's colour
            - one rectangle in the FRAME_COLOUR to frame it at the same
              dimensions, but with a specified thickness of 3
        and (2) one additional rectangle to frame this Block in the
        HIGHLIGHT_COLOUR at a thickness of 5 if this block has been
        selected for action, that is, if its highlighted attribute is True.

        The rectangles are in the format required by method Renderer.draw.
        Each tuple contains:
        - the colour of the rectangle
        - the (x, y) coordinates of the top left corner of the rectangle
        - the (height, width) of the rectangle, which for our Blocky game
          will always be the same
        - an int indicating how to render this rectangle. If 0 is specified
          the rectangle will be filled with its colour. If > 0 is specified,
          the rectangle will not be filled, but instead will be outlined in
          the FRAME_COLOUR, and the value will determine the thickness of
          the outline.

        The order of the rectangles does not matter.
        """
        # If the block is highlighted then highlight colour is used
        rectangles = []
        if self.highlighted is True:
            rectangles.append(
                (HIGHLIGHT_COLOUR, self.position, (self.size,
                                                   self.size), 5))
        # else, following the specified docstrings
        if not self.children:
            rectangles.extend(
                [(self.colour, self.position, (self.size, self.size), 0),
                 (FRAME_COLOUR, self.position, (self.size, self.size), 3)])
        else:
            for i in self.children:
                rectangles.extend(i.rectangles_to_draw())
        return rectangles

    def swap(self, direction: int) -> None:
        """Swap the child Blocks of this Block.

        If <direction> is 1, swap vertically.  If <direction> is 0, swap
        horizontally. If this Block has no children, do nothing.
        """
        if self.children:
            child_1, child_2, child_3, child_4 = self.children[0], \
                                             self.children[1], \
                                             self.children[2], self.children[3]
            if direction == 0:
                self.children[0], self.children[1], self.children[2], self. \
                    children[3] = child_2, child_1, child_4, child_3
            elif direction == 1:
                self.children[0], self.children[1], self.children[2], self. \
                    children[3] = child_4, child_3, child_2, child_1
            self.update_block_locations(self.position, self.size)
        else:
            pass

    def rotate(self, direction: int) -> None:
        """Rotate this Block and all its descendants.

        If <direction> is 1, rotate clockwise.  If <direction> is 3, rotate
        counterclockwise. If this Block has no children, do nothing.
        """
        if self.children:
            child_1, child_2, child_3, child_4 = self.children[0], \
                                                 self.children[1], \
                                                 self.children[2], \
                                                 self.children[3]
            if direction == 1:
                self.children[0], self.children[1], self.children[2], self. \
                    children[3] = child_2, child_3, child_4, child_1
            elif direction == 3:
                self.children[0], self.children[1], self.children[2], self. \
                    children[3] = child_4, child_1, child_2, child_3
            else:
                for child in self.children:
                    child.rotate(direction)
            self.update_block_locations(self.position, self.size)
        else:
            pass

    def smash(self) -> bool:
        """Smash this block.

        If this Block can be smashed,
        randomly generating four new child Blocks for it.  (If it already
        had child Blocks, discard them.)
        Ensure that the RI's of the Blocks remain satisfied.

        A Block can be smashed iff it is not the top-level Block and it
        is not already at the level of the maximum depth.

        Return True if this Block was smashed and False otherwise.
        """
        if self.level == 0 or self.level == self.max_depth:
            return False
        else:
            self.colour = None
            child_1 = random_init(self.level, self.max_depth)
            child_2 = random_init(self.level, self.max_depth)
            child_3 = random_init(self.level, self.max_depth)
            child_4 = random_init(self.level, self.max_depth)
            self.children = child_1.children + child_2.children + child_3.\
                children + child_4.children
            self.update_block_locations(self.position, self.size)
            return True

    def update_block_locations(self, top_left: Tuple[int, int],
                               size: int) -> None:
        """
        Update the position and size of each of the Blocks within this Block.

        Ensure that each is consistent with the position and size of its
        parent Block.

        <top_left> is the (x, y) coordinates of the top left corner of
        this Block.  <size> is the height and width of this Block.
        """
        # size and position should be initialized no matter what because
        # there will always be a root Block
        self.size = size
        self.position = top_left
        # if there are no children updating the location is not needed
        if not self.children:
            pass
        # calculate the position of the blocks given the position of the parent
        # block and its size. Half the size of the children blocks
        else:
            for _ in self.children:
                half_size = round(self.size / 2)
                x = top_left[0]
                y = top_left[1]
                half_xy = (top_left[0] + half_size, top_left[1] + half_size)
                half_x = top_left[0] + half_size
                half_y = top_left[1] + half_size
                children = self.children
                children[0].update_block_locations((half_x, y), half_size)
                children[1].update_block_locations((x, y), half_size)
                children[2].update_block_locations((x, half_y), half_size)
                children[3].update_block_locations(half_xy, half_size)

    def get_selected_block(self, location: Tuple[int, int], level: int) \
            -> 'Block':
        """Return the Block within this Block that includes the given location
        and is at the given level. If the level specified is lower than
        the lowest block at the specified location, then return the block
        at the location with the closest level value.

        <location> is the (x, y) coordinates of the location on the window
        whose corresponding block is to be returned.
        <level> is the level of the desired Block.  Note that
        if a Block includes the location (x, y), and that Block is subdivided,
        then one of its four children will contain the location (x, y) also;
        this is why <level> is needed.

        Preconditions:
        - 0 <= level <= max_depth
        """
        if self.level == level:
            return self
        elif not self.children:
            return self
        else:
            mid_x = (self.position[0] + round(self.size / 2))
            mid_y = (self.position[1] + round(self.size / 2))
            location_x = location[0]
            location_y = location[1]
            for _ in range(len(self.children)):
                if mid_x <= location_x and mid_y > location_y:
                    return self.children[0].get_selected_block(location, level)
                elif mid_x > location_x and mid_y > location_y:
                    return self.children[1].get_selected_block(location,
                                                               level)
                elif mid_x > location_x and mid_y <= location_y:
                    return self.children[2].get_selected_block(location,
                                                               level)
                elif mid_x <= location_x and mid_y <= location_y:
                    return self.children[3].get_selected_block(location,
                                                               level)

    def flatten(self) -> List[List[Tuple[int, int, int]]]:
        """Return a two-dimensional list representing this Block as rows
        and columns of unit cells.

        Return a list of lists L, where, for 0 <= i, j <
        2^{max_depth - self.level}
            - L[i] represents column i and
            - L[i][j] represents the unit cell at column i and row j.
        Each unit cell is represented by 3 ints for the colour
        of the block at the cell location[i][j]

        L[0][0] represents the unit cell in the upper left corner of the Block.
        """
        if not self.children:
            lst = [
                self.colour for _ in range(2 ** (self.max_depth - self.level))]
            return [lst for _ in range(2 ** (self.max_depth - self.level))]
        else:
            child1 = self.children[0].flatten()
            child2 = self.children[1].flatten()
            child3 = self.children[2].flatten()
            child4 = self.children[3].flatten()
            flatten_lst = [
                child2[column_l] + child3[column_l] for column_l in
                range(len(child2))]
            flatten_lst.extend([child1[column_r] + child4[column_r] for
                                column_r in range(len(child1))])

            return flatten_lst


def random_init(level: int, max_depth: int) -> 'Block':
    """Return a randomly-generated Block with level <level> and subdivided
    to a maximum depth of <max_depth>.

    Throughout the generated Block, set appropriate values for all attributesx
    except position and size.  They can be set by the client, using method
    update_block_locations.

    Precondition:
    level <= max_depth
    if level 0 and max_depth is 3 what happens?
    """
    # generated a random_colour, and a real before 0, and 1
    random_, random_colour = random.random(), random.choice(COLOUR_LIST)

    # base case to check if level is the same as the max_depth
    # updating the blocks.max_depth to get a universal max_depth
    if level == max_depth:
        block = Block(level, random_colour, [])
        block.max_depth = max_depth
        return block
    # second base case uses the formula to determine if it should
    # generate no children
    elif not random_ < math.exp(-0.25 * level):
        block = Block(level, random_colour, [])
        block.max_depth = max_depth
        return block
    # else case could be written elif level != max_depth and random <
    # math.exp(-0.25 * level). Makes the children recursively at level + 1
    # until it reaches either base case while updating blocks max_depth
    # while at it. Creating a self.children for the top-level Block
    else:
        block = Block(level, None, [])
        child_1 = random_init(level + 1, max_depth)
        child_2 = random_init(level + 1, max_depth)
        child_3 = random_init(level + 1, max_depth)
        child_4 = random_init(level + 1, max_depth)
        child_1.parent = child_2.parent = child_3.parent = child_4.parent = \
            block
        block.max_depth = child_1.max_depth = child_2.max_depth = \
            child_3.max_depth = child_4.max_depth = max_depth
        block.children.extend([child_1, child_2, child_3, child_4])
        return block


def attributes_str(b_: Block, verbose) -> str:
    """Return a str that is a concise representation of the attributes of <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Note: These are attributes that every Block has.
    """
    answer = f'pos={b_.position}, size={b_.size}, level={b_.level}, '
    if verbose:
        answer += f'highlighted={b_.highlighted}, max_depth={b_.max_depth}'
    return answer


def print_block(b_: Block, verbose=False) -> None:
    """Print a text representation of Block <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    print_block_indented(b_, 0, verbose)


def print_block_indented(b_: Block, indent: int, verbose) -> None:
    """Print a text representation of Block <b>, indented <indent> steps.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    if len(b_.children) == 0:
        # b a leaf.  Print its colour and other attributes
        print(f'{"  " * indent}{colour_name(b_.colour)}: ' +
              f'{attributes_str(b_, verbose)}')
    else:
        # b is not a leaf, so it doesn't have a colour.  Print its
        # other attributes.  Then print its children.
        print(f'{"  " * indent}{attributes_str(b_, verbose)}')
        for child in range(len(b_.children)):
            print_block_indented(b_.children[child], indent + 1, verbose)


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-io': ['print_block_indented'],
    #     'allowed-import-modules': [
    #         'doctest', 'python_ta', 'random', 'typing',
    #         'block', 'goal', 'player', 'renderer', 'math'
    #     ],
    #     'max-attributes': 15
    # })

    # This tiny tree with one node will have no children, highlighted False,
    # and will have the provided values for level and colour; the initializer
    # sets all else (position, size, and max_depth) to 0.
    b0 = Block(0, COLOUR_LIST[2])
    # Now we update position and size throughout the tree.
    b0.update_block_locations((0, 0), 750)
    print("=== tiny tree ===")
    # We have not set max_depth to anything meaningful, so it still has the
    # value given by the initializer (0 and False).
    print_block(b0, True)

    b1 = Block(0, children=[
        Block(1, children=[
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, COLOUR_LIST[2]),
        Block(1, children=[
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[1])
        ])
    ])
    b1.update_block_locations((0, 0), 750)
    print("\n=== handmade tree ===")
    # Similarly, max_depth is still 0 in this tree.  This violates the
    # representation invariants of the class, so we shouldn't use such a
    # tree in our real code, but we can use it to see what print_block
    # does with a slightly bigger tree.
    print_block(b1, True)

    # Now let's make a random tree.
    # random_init has the job of setting all attributes except position and
    # size, so this time max_depth is set throughout the tree to the provided
    # value (3 in this case).
    b2 = random_init(0, 3)
    # Now we update position and size throughout the tree.
    b2.update_block_locations((0, 0), 750)
    print("\n=== random tree ===")
    # All attributes should have sensible values when we print this tree.
    print_block(b2, True)



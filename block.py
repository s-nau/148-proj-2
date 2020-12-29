"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the Block class, the main data structure used in the game.
"""
from __future__ import annotations
from typing import Optional, Tuple, List, Union
import random
import math

from settings import colour_name, COLOUR_LIST


def generate_board(max_depth: int, size: int) -> Block:
    """Return a new game board with a depth of <max_depth> and dimensions of
    <size> by <size>.

    >>> board = generate_board(3, 750)
    >>> board.max_depth
    3
    >>> board.size
    750
    >>> len(board.children) == 4
    True
    """
    board = Block((0, 0), size, random.choice(COLOUR_LIST), 0, max_depth)
    board.smash()

    return board


class Block:
    """A square Block in the Blocky game, represented as a tree.

    In addition to its tree-related attributes, a Block also contains attributes
    that describe how the Block appears on a Cartesian plane. All positions
    describe the upper left corner (x, y), and the origin is at (0, 0). All
    positions and sizes are in the unit of pixels.

    When a block has four children, the order of its children impacts each
    child's position. Indices 0, 1, 2, and 3 are the upper-right child,
    upper-left child, lower-left child, and lower-right child, respectively.

    === Public Attributes ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
    size:
        The height and width of this square Block.
    colour:
        If this block is not subdivided, <colour> stores its colour. Otherwise,
        <colour> is None.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero. If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    children:
        The blocks into which this block is subdivided. The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.

    === Representation Invariants===
    - len(children) == 0 or len(children) == 4
    - If this Block has children:
        - their max_depth is the same as that of this Block.
        - their size is half that of this Block.
        - their level is one greater than that of this Block.
        - their position is determined by the position and size of this Block,
          and their index in this Block's list of children.
        - this Block's colour is None.
    - If this Block has no children:
        - its colour is not None.
    - level <= max_depth
    """
    position: Tuple[int, int]
    size: int
    colour: Optional[Tuple[int, int, int]]
    level: int
    max_depth: int
    children: List[Block]

    def __init__(self, position: Tuple[int, int], size: int,
                 colour: Optional[Tuple[int, int, int]], level: int,
                 max_depth: int) -> None:
        """Initialize this block with <position>, dimensions <size> by <size>,
        the given <colour>, at <level>, and with no children.

        Preconditions:
            - position[0] >= 0 and position[1] >= 0
            - size > 0
            - level >= 0
            - max_depth >= level
        """
        self.position = position
        self.size = size
        self.colour = colour
        self.level = level
        self.max_depth = max_depth
        self.children = []

    def __str__(self) -> str:
        """Return this Block in a string format.

        >>> block = Block((0, 0), 750, (0, 0, 0), 0, 1)
        >>> str(block)
        'Leaf: colour=Black, pos=(0, 0), size=750, level=0\\n'
        """
        if len(self.children) == 0:
            indents = '\t' * self.level
            colour = colour_name(self.colour)
            return f'{indents}Leaf: colour={colour}, pos={self.position}, ' \
                   f'size={self.size}, level={self.level}\n'
        else:
            indents = '\t' * self.level
            result = f'{indents}Parent: pos={self.position},' \
                     f'size={self.size}, level={self.level}\n'

            for child in self.children:
                result += str(child)

            return result

    def __eq__(self, other: Block) -> bool:
        """Return True iff this Block and all its descendents are equivalent to
        the <other> Block and all its descendents.
        """
        if len(self.children) == 0 and len(other.children) == 0:
            # Both self and other are leaves.
            return self.position == other.position and \
                   self.size == other.size and \
                   self.colour == other.colour and \
                   self.level == other.level and \
                   self.max_depth == other.max_depth
        elif len(self.children) != len(other.children):
            # One of self or other is a leaf while the other is not.
            return False
        else:
            # Both self and other have four children.
            for i in range(4):
                # The != operator also uses the __eq__ special method.
                if self.children[i] != other.children[i]:
                    return False

            return True

    def _child_size(self) -> int:
        """Return the size of this Block's children.
        """
        return round(self.size / 2.0)

    def _children_positions(self) -> List[Tuple[int, int]]:
        """Return the positions of this Block's four children.

        The positions are returned in this order: upper-right child, upper-left
        child, lower-left child, lower-right child.
        """
        x = self.position[0]
        y = self.position[1]
        size = self._child_size()

        return [(x + size, y), (x, y), (x, y + size), (x + size, y + size)]

    def _update_children_positions(self, position: Tuple[int, int]) -> None:
        """Set the position of this Block to <position> and update all its
        descendants to have positions consistent with this Block's.

        <position> is the (x, y) coordinates of the upper-left corner of this
        Block.
        """
        if self.children == []:
            self.position = position
        else:
            self.position = position
            x = position[0]
            y = position[1]
            size = self._child_size()
            self.children[0].position = (x + size, y)
            self.children[1].position = (x, y)
            self.children[2].position = (x, y + size)
            self.children[3].position = (x + size, y + size)
            for i in range(len(self.children)):
                pos = self.children[i].position
                self.children[i]._update_children_positions(pos)


    def smashable(self) -> bool:
        """Return True iff this block can be smashed.

        A block can be smashed if it has no children and its level is not at
        max_depth.
        """
        return self.level != self.max_depth and len(self.children) == 0

    def smash(self) -> bool:
        """Sub-divide this block so that it has four randomly generated
        children.

        If this Block's level is <max_depth>, do nothing. If this block has
        children, do nothing.
        
        Return True iff the smash was performed.
        """
        # if not self.smashable():
        #     return False
        # else:
        #     rand_num = random.random()
        #     lev = self.level
        #     if rand_num < math.exp(-0.25 * lev):
        #         self.smash()
        #     else:
        #         color = random.choice(COLOUR_LIST)
        #         self.colour = color
        #     for child in self.children:
        #         child.smash()
        #     return True
        if self.children != []: # has children
            return False
        elif self.level == self.max_depth: # at max depth
            return False
        else:  # not at greatest level, and has no children
            self._children_color_generator()
                # sets colour to None
            for child in self.children:
                num = random.random()
                if num < math.exp(-0.25 * (self.level + 1)):
                        # randomly smashing the lower blocks as the
                        # lower blocks aren't
                        # necessarily solid
                    child.smash()
            return True

    def _children_color_generator(self) -> None:
        """mutates the children of block, to have randomly generated
        colors of children
        precondiction block has no children
        >>> block1 = Block((0,0), 2, COLOUR_LIST[0], 0, 1)
        >>> block1.children == []
        True
        >>> block1._children_color_generator()
        >>> block1.children != []
        True
        """
        lst = []
        level = self.level + 1
        max_depth = self.max_depth
        position = self.position
        size = self._child_size()
        self.colour = None
        x = position[0]
        y = position[1]
        #
        for i in range(4):
            color = random.choice(COLOUR_LIST)
            # need a random color
            if i == 0: # first block
                pos = (x + size, y)
            elif i == 1: # second block
                pos = (x, y)
            elif i == 2: # third block
                pos = (x, y + size)
            else: # fourth blcok
                pos = (x + size, y + size)
            to_append = Block(pos, size, color, level, max_depth)
            # block with the attributes
            lst.append(to_append)
            # for the list of blocks
        self.children = lst


    def swap(self, direction: int) -> bool:
        """Swap the child Blocks of this Block.

        If this Block has no children, do nothing. Otherwise, if <direction> is
        1, swap vertically. If <direction> is 0, swap horizontally.
        
        Return True iff the swap was performed.

        Precondition: <direction> is either 0 or 1
        """
        deep_copy = self.create_copy()
        if self.children == []:
            return False
        elif direction == 1: # swithc vertical
            self.children[0]._update_children_positions(
                deep_copy.children[3].position)
            # upper right childr to lower right
            self.children[1]._update_children_positions(deep_copy.children[2].
                                                        position)
            # upper left child to lwer left
            self.children[2]._update_children_positions(deep_copy.children[1]
                                                        .position)
            # lower left childr to upper left
            self.children[3]._update_children_positions(deep_copy.children[0].
                                                        position)
            # lower right child to upper right
            self._update_children_lst(self.children[3], self.children[2],
                                      self.children[1], self.children[0])
            return True
        else:  # switch horizontal dircetion == 0
            self.children[0]._update_children_positions(deep_copy.children[1]
                                                        .position)
            # upper right to upper left
            self.children[1]._update_children_positions(deep_copy.children[0]
                                                        .position)
            # upper left to upper right
            self.children[2]._update_children_positions(deep_copy.children[3].
                                                        position)
            # lower left to lower right
            self.children[3]._update_children_positions(deep_copy.children[2].
                                                        position)
            # lower right to lower left
            self._update_children_lst(self.children[1], self.children[0],
                                      self.children[3], self.children[2])
            return True



    def rotate(self, direction: int) -> bool:
        """Rotate this Block and all its descendants.

        If this Block has no children, do nothing. If <direction> is 1, rotate
        clockwise. If <direction> is 3, rotate counter-clockwise.
        
        Return True iff the rotate was performed.

        Precondition: <direction> is either 1 or 3.
        """
        if self.children == []:
            return False
        elif direction == 3:
            self._counter_clockwise_rotation()
            self._update_children_positions(self.position)
            for child in self.children:
                child.rotate(3)
            return True
        else:  # direction = 1
            self._clockwise_rotation()
            self._update_children_positions(self.position)
            for child in self.children:
                child.rotate(1)
            return True


    def _counter_clockwise_rotation(self) -> None:
        """rotates the children of the block counter clockwise
        precondition block has children
        >>> block1 = Block((0,0), 2, None, 0, 1)
        >>> block1._children_color_generator()
        >>> block1_copy = block1.create_copy()
        >>> block1._counter_clockwise_rotation()
        >>> block1_copy.children[0].colour == block1.children[1].colour
        True
        >>> block1_copy.children[1].colour == block1.children[2].colour
        True
        """
        #already know block has children
        deep_copy = self.create_copy()
        self.children[0].position = deep_copy.children[1].position
        self.children[1].position = deep_copy.children[2].position
        self.children[2].position = deep_copy.children[3].position
        self.children[3].position = deep_copy.children[0].position
        self._update_children_lst(self.children[3], self.children[0],
                                  self.children[1], self.children[2])

    def _clockwise_rotation(self) -> None:
        """rotates the children of the block clockwise
        precondition block has children
        >>> block1 = Block((0,0), 2, None, 0, 1)
        >>> block1._children_color_generator()
        >>> block1_copy = block1.create_copy()
        >>> block1._clockwise_rotation()
        >>> block1.children[3].colour == block1_copy.children[0].colour
        True
        >>> block1.children[0].colour ==  block1_copy.children[1].colour
        True
        """
        # already know block has children
        deep_copy = self.create_copy()
        self.children[0].position = deep_copy.children[3].position
        self.children[1].position = deep_copy.children[0].position
        self.children[2].position = deep_copy.children[1].position
        self.children[3].position = deep_copy.children[2].position
        # changes location in the tree
        self._update_children_lst(self.children[1], self.children[2],
                                  self.children[3], self.children[0])


    def paint(self, colour: Tuple[int, int, int]) -> bool:
        """Change this Block's colour iff it is a leaf at a level of max_depth
        and its colour is different from <colour>.

        Return True iff this Block's colour was changed.
        """
        if self.level != self.max_depth:
            return False
        elif self.colour == colour:
            return False
        else:
            self.colour = colour
            return True

    def combine(self) -> bool:
        """Turn this Block into a leaf based on the majority colour of its
        children.

        The majority colour is the colour with the most child blocks of that
        colour. A tie does not constitute a majority (e.g., if there are two red
        children and two blue children, then there is no majority colour).

        If there is no majority colour, do nothing. If this block is not at a
        level of max_depth - 1, or this block has no children, do nothing.

        Return True iff this Block was turned into a leaf node.
        """
        if self.children == []:
            return False
        elif self.level != (self.max_depth - 1):
            return False
        elif not self._majority_children_color():
            return False
        else:
            color = self._majority_children_color()
            # already know that doesn't evaluate to false
            self.position = self._children_positions()[1]
            #because postion will be top left
            self.colour = color
            # color of children majority
            self.children = []
            # no children

            return True

    def _majority_children_color(self) -> Union[bool, Tuple[int, int, int]]:
        """returns the false, iff there is no majority color of a blocks
         children, otherwise it returns the majority color of the blocks
          children, a tie means no majority
        precondition self has children
        >>> block1 = Block((0,0), 2, None, 0, 1)
        >>> block1._children_color_generator()
        >>> block1_copy = block1.create_copy()
        >>> block1.children[0].colour = COLOUR_LIST[0]
        >>> block1.children[1].colour = COLOUR_LIST[0]
        >>> block1.children[2].colour = COLOUR_LIST[0]
        >>> block1._majority_children_color() == COLOUR_LIST[0]
        True
        >>> block1_copy.children[0].colour = COLOUR_LIST[0]
        >>> block1_copy.children[1].colour = COLOUR_LIST[1]
        >>> block1_copy.children[2].colour = COLOUR_LIST[2]
        >>> block1_copy.children[3].colour = COLOUR_LIST[3]
        >>> block1_copy._majority_children_color()
        False
        """
        lst_of_child_colors = []
        for child in self.children:
            lst_of_child_colors.append(child.colour)
        # shallow copy of all the children colors
        dict_of_color_to_appearance = {}
        for color in lst_of_child_colors:
            if color not in dict_of_color_to_appearance:
                dict_of_color_to_appearance[color] = 1
            else:
                dict_of_color_to_appearance[color] += 1
        # dictionary of color to appearance
        color_counter = 0  # need to compare to find highest frequency
        highest = (0, 0, 0)
        for color in dict_of_color_to_appearance:
            if dict_of_color_to_appearance[color] > color_counter:
                color_counter = dict_of_color_to_appearance[color]
                highest = color
        if len(dict_of_color_to_appearance) == len(lst_of_child_colors):
            # [1,2,3,4]
            return False
        elif len(dict_of_color_to_appearance) == 1: # [1,1,1,1]
            return lst_of_child_colors[0]
        elif color_counter == 3: # therefore [ 1,1,1,2]
            return highest
        elif color_counter == 2:
            if len(dict_of_color_to_appearance) == 2: # therefore tie
                return False
            else:  # therefore [1,1,2,3]
                return highest
        return None

    def create_copy(self) -> Block:
        """Return a new Block that is a deep copy of this Block.

        Remember that a deep copy has new blocks (not aliases) at every level.
        """
        pos = self.position
        size = self.size
        color = self.colour
        level = self.level
        max_depth = self.max_depth
        if self.children == []:
            new_block = Block(pos, size, color, level, max_depth)
            # block that is a deep copy of the original block
            return new_block
        else:
            new_block = Block(pos, size, color, level, max_depth)
            for child in self.children:
                new_block.children.append(child.create_copy())
                # recursive deep copy of the children
            return new_block


    def _update_children_lst(self, first: Block, second: Block, third: Block,
                             fourth: Block) -> None:
        """changes the order of self.children to the order of [<first>,
        <second>, <third>, <fourth>]
        precondition the blocks of first, second etc.postions are already
        set where they will be once they are reordered
        >>> parent_block = Block((0,0), 2, None, 0, 1)
        >>> child_block1 = Block((1,0), 1, COLOUR_LIST[0], 1, 1)
        >>> child_block2 = Block((0,0), 1, COLOUR_LIST[0], 1, 1)
        >>> child_block3 = Block((0,1), 1, COLOUR_LIST[0], 1, 1)
        >>> child_block4 = Block((1,1), 1, COLOUR_LIST[0], 1, 1)
        >>> parent_block.children == []
        True
        >>> parent_block._update_children_lst(child_block1, child_block2,
        ... child_block3, child_block4)
        >>> parent_block.children == [child_block1, child_block2,
        ... child_block3, child_block4]
        True

        """
        copy1 = first.create_copy()
        copy2 = second.create_copy()
        copy3 = third.create_copy()
        copy4 = fourth.create_copy()
        self.children[0] = copy1
        self.children[1] = copy2
        self.children[2] = copy3
        self.children[3] = copy4




if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', '__future__', 'math',
            'settings'
        ],
        'max-attributes': 15,
        'max-args': 6
    })

    # This is a board consisting of only one block.
    b1 = Block((0, 0), 750, COLOUR_LIST[0], 0, 1)
    print("=== tiny board ===")
    print(b1)

    # Now let's make a random board.
    b2 = generate_board(3, 750)
    print("\n=== random board ===")
    print(b2)

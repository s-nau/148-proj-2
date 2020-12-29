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

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    target_goal = random.choice([PerimeterGoal, BlobGoal])
    lst_of_goals = []
    lst_of_colors = []
    while len(lst_of_goals) < num_goals:
        color = random.choice(COLOUR_LIST)
        if color not in lst_of_colors:
            lst_of_goals.append(target_goal(color))
            lst_of_colors.append(color)
    return lst_of_goals


# def _unit_block_to_postion_builder(block: Block) -> \
    #     list[Block, tuple[int, int]]:
    #
    # unit_block_to_pos = []
    # if block.level == block.max_depth:
    #     unit_block_to_pos.append((block, block.position))
    # else:
    #     for child in block.children:
    #         unit_block_to_pos.extend(_unit_block_to_postion_builder(child))
    # return unit_block_to_pos



def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    squares_side = int((2 ** block.max_depth) / (2 ** block.level))
    lst = []
    for _ in range(squares_side):
        sublist = []
        for _ in range(squares_side):  # correct number of sublists
            sublist.append(0)
        lst.append(sublist)
    _flatten_helper_function(block, lst, 0, 0)
    return lst

def _flatten_helper_function(block: Block, lst: List[List], loc_x: int,
                             loc_y: int) \
        -> None:
    """mutates the list <lst> with the block colours within <block> that are
    between loc_x and (2 ** block.max_depth) / (2 ** block.level) and loc_y and
    (2 ** block.max_depth) / (2 ** block.level) inclusive. lst is a lst with
    the number of cells that are equal to the total spots that could be filled
    precondition: lst has the expected dimensions for block, as in if
    block was a block with max depth 1, the dimensions of lst would be
    [[_, _], [_, _]
    >>> block1 = Block((0,0), 2, (1, 128, 181), 0, 1)
    >>> lst = [[0 ,0], [0, 0]]
    >>> _flatten_helper_function(block1, lst, 0 , 0)
    >>> lst[0][0] == block1.colour and lst[0][1] == block1.colour
    True
    >>> lst[1][1] == block1.colour and lst[1][0] == block1.colour
    True
    >>> block2 = Block((0,0), 2, (1, 128, 181), 0, 0)
    >>> lst2 = [[0]]
    >>> _flatten_helper_function(block2, lst2, 0 ,0 )
    >>> lst2[0][0] == block2.colour
    True
    """
    # if block.level == block.max_depth:
    #
    if block.children == []:
        squares_side = int((2 ** block.max_depth) / (2 ** block.level))
        for i in range(squares_side):
            for j in range(squares_side):
                lst[i + loc_x][j + loc_y] = block.colour
    else:
        squares_side = int(int((2 ** block.max_depth) / (2 ** block.level)) / 2)
        _flatten_helper_function(block.children[1], lst, loc_x, loc_y)
        # top left
        _flatten_helper_function(block.children[0], lst, loc_x + squares_side,
                                 loc_y)
        # top right
        _flatten_helper_function(block.children[2], lst, loc_x, loc_y +
                                 squares_side)
        # bottom left
        _flatten_helper_function(block.children[3], lst, loc_x + squares_side,
                                 loc_y + squares_side)
        # bottom right

    # block_copy = block.create_copy()
    # _lowest_units(block_copy)
    # lst = []
    # if block_copy.level == block_copy.max_depth:
    #     if block_copy.level == 0: # max depth is 0
    #         lst.append([block_copy.colour])
    #     else:
    #         lst.append(block_copy.colour)
    # # elif block.children == []: # no children and not at max level
    # #     sub_list = []
    # #     dif = (block.max_depth - block.level) * 2
    # #     # the number of sub blocks
    # #     for i in range(dif): # correct number of columns and rows
    # #         to_append = []
    # #         for j in range(dif):
    # #             to_append.append(block.colour)
    # #         sub_list.append(to_append)
    # #     lst.append(sub_list)
    # else:  # not at max depth
    #     top_left = _flatten(block_copy.children[1])
    #     top_right = _flatten(block_copy.children[0])
    #     bottom_right = _flatten(block_copy.children[3])
    #     bottom_left = _flatten(block_copy.children[2])
    #     top_left.extend(bottom_left)
    #     bottom_right.extend(bottom_right)
    #     lst.append(top_left)
    #     lst.append(top_right)
    # return lst



    # block_copy = block.create_copy()
    # _lowest_units(block_copy)  # this mutates block-copy
    # # don't want to mutate block
    # to_return = []
    # size = int(block_copy.size / (block_copy.max_depth * 2))
    # # the size of each of the child blocks
    # lst_of_cords = _coord_builder(block_copy)
    # for i in range(block_copy.max_depth * 2):  # expected number of cells
    #     lst_of_cords.append(i * size)
    # # the list of the coordinates
    # if block_copy.max_depth == 0: # the single unit works differently
    #     return [[block_copy.colour]]
    # else:  # have to iterate the proper amount of times
    #     for j in range(block_copy.max_depth * 2):
    #         lst = _col_builder(block_copy, lst_of_cords[j])
    #         # list of column blocks
    #         lst[0] = lst[0].colour  # need to convert them all to colors
    #         lst[1] = lst[1].colour
    #         lst[2] = lst[2].colour
    #         lst[3] = lst[3].colour
    #         to_return.append(lst)
    # return to_return


#         # else:
#         #     x = block_copy_max.position[0]
#         #     y = block_copy_max.position[1]
#         #
#         #     top_left = _flatten(block_copy_max.children[1])
#         #     top_right = _flatten(block_copy_max.children[0])
#         #     bottom_left = _flatten(block_copy_max.children[2])
#         #     bottom_right = _flatten(block_copy_max.children[3])
#         #     top_right.extend(bottom_right)
#         #     top_left.extend(bottom_left)
#         #     to_return.insert(0, top_left)
#         #     to_return.insert(1, top_right)
#         # return to_return
#         # x = block_copy.position[0]
#         # y = block_copy.position[1]
#         # child_size = int(block.size / 2)
#         # lst_of_cords = [] # lst of cords
#         # for i in range(len(block_copy.children)):
#         #     lst_of_cords.append(child_size *
#         #     block_copy.children[i].position[0])
#         # for i in range(len(block_copy.children)):
#
#
# def _col_builder(block: Block, num: int) -> Optional[List[Block]]:
#     """returns the cells of block who have a x coordinate of num, if there are
#     no cells that satisfy this column then returns None
#      >>> par_block = Block((0,0), 2, None, 0, 1,)
#      >>> child_block_0 = Block((1,0), 1, COLOUR_LIST[0], 1, 1)
#      >>> child_block_1 = Block((0,0), 1, COLOUR_LIST[1], 1, 1)
#      >>> child_block_2 = Block((0,1), 1, COLOUR_LIST[2], 1, 1)
#      >>> child_block_3 = Block((1,1), 1, COLOUR_LIST[3], 1, 1)
#      >>> par_block.children.extend([child_block_0, child_block_1,
#      ... child_block_2, child_block_3])
#      >>> _col_builder(par_block, 0) == [child_block_1, child_block_2]
#      True
#      >>> _col_builder(par_block, 3)
#      >>> _col_builder(par_block, 1) == [child_block_0, child_block_]
#      True
#      """
#     lst = []
#     if block.level == block.max_depth:
#         if block.position[0] == num:
#             # weird behavior with rounding
#             lst.append(block)
#         else:
#             return None
#     else:
#         for child in block.children:
#             if _col_builder(child, num) is not None:
#                 # if none that means doesn't include
#                 lst.extend(_col_builder(child, num))
#
#     if len(lst) == 0:
#         return None
#     else:
#         return lst
#
# """
#         # block_copy.level == (block_copy.max_depth - 1):
#         # pos_x = block_copy.position[0]
#         # pos_y = block_copy.position[1]
#         # size_children = block_copy.children[0].size
#         # lst_of_cords = []
#         # for i in range(len(block_copy.children)):
#         #     lst_of_cords.append(i * size_children)
#         # for i in range(len(block_copy.children)):
#         #     if block_copy.children[i].position[0] == pos_x and \
#         #                     block_copy.children[i].position[1] == pos_y:
#         #         to_return.insert()
#
#     # else:
#     #
#     #     # proper ordering
#     #     top_left = _flatten(block_copy.children[1])
#     #     bottom_left = _flatten(block_copy.children[2])
#     #     top_right = _flatten(block_copy.children[0])
#     #     bottom_right = _flatten(block_copy.children[3])
#     #     top_left.extend(bottom_left)
#     #     first_col = top_left  # already extended
#     #     top_right.extend(bottom_right)
#     #     second_col = top_right # already extended
#     #     to_return.append(first_col)
#     #     to_return.append(second_col)
#     # return to_return
#
#
#         # for child in children_reordered:
#         #     to_return.append(_flatten(child))
#     # for i in range(len(to_return)):
#     #     if isinstance(to_return[i][0], list):
#     #         flattened = []
#     #         for sublist in to_return[i]:
#     #             flattened.append(sublist[0])
#     #         to_return[i] = flattened
#     # return to_return
# """
# def _lowest_units(block: Block) -> None:
#     """mutates the block subdivided into the lowest level possible, where
#     each lower block takes the parent blocks color, if the block has no
#     children
#
#     >>> block1 = Block((0,0), 2, COLOUR_LIST[0], 0, 1)
#     >>> block1_copy = block1.create_copy()
#     >>> block_child1 = Block((1,0), 1, COLOUR_LIST[0], 1, 1)
#     >>> block_child2 = Block((0,0), 1, COLOUR_LIST[0], 1, 1)
#     >>> block_child3 = Block((0,1), 1, COLOUR_LIST[0], 1, 1)
#     >>> block_child4 = Block((1,1), 1, COLOUR_LIST[0], 1, 1)
#     >>> block1_copy.children.extend([block_child1, block_child2, block_child3,
#     ... block_child4])
#     >>> block1_copy.colour = None
#     >>> _lowest_units(block1) == block1_copy
#     True
#     """
#     if block.level == block.max_depth:
#         return block
#     elif block.children != []: # not at max depth, but has children
#         for child in block.children:
#             _lowest_units(child)
#     else: # level is not max
#         size = round(block.size / 2)
#         colour = block.colour
#         level = block.level + 1
#         max_depth = block.max_depth
#         pos_x = block.position[0]
#         pos_y = block.position[1]
#         for i in range(4):
#             if i == 0:
#                 pos = (pos_x + size, pos_y)
#             elif i == 1:
#                 pos = (pos_x, pos_y)
#             elif i == 2:
#                 pos = (pos_x, pos_y + size)
#             else:
#                 pos = (pos_x + size, pos_y + size)
#             new_child = Block(pos, size, colour, level, max_depth)
#             block.children.append(new_child)
#         block.colour = None
#         for child in block.children:
#             _lowest_units(child)
#     return None
# #     # for i in range(len(lst_to_return)):
# #     #     if isinstance(lst_to_return[i][0], list):
# #     #         flattened = []
# #     #         for sublist in lst_to_return[i]:
# #     #             flattened.append(sublist[0])
# #     #         lst_to_return[i] = flattened
#
# def _coord_builder(block:Block)-> List[int]:
#     """returns the unique x coordinates of block and it's descedents
#     >>> block = Block((0,0), 1, COLOUR_LIST[0], 0, 0)
#     >>> _coord_builder(block)
#     [0]
#     >>> block2 = Block((0,0), 2, None, 0, 1)
#     >>> _lowest_units(block2)
#     >>> _coord_builder(block2)
#     [0, 1]
#     """
#     lst = []
#     if block.level == block.max_depth:
#         return [block.position[0]]
#     else:
#         for children in block.children:
#             lst.extend(_coord_builder(children))
#         return list(set(lst))
# """
#     # if block.level == block.max_depth:
#     #     return [[block.color]]
#     # elif
#     # max_depth = block.max_depth
#     # if max_depth == 0:
#     #     return [block.colour]
#     # to_return = []
#     # lst_of_unit_blocks = _unit_block_to_postion_builder(block)
#     # unit_block_size = int(block.size / (max_depth * 2))
#     # # size of the unit blocks
#     # lst_of_starting_x = []
#     # for i in range(max_depth):
#     #     lst_of_starting_x.append(i * unit_block_size)
#     # lst_of_starting_y = []
#     # for i in range(max_depth):
#     #     lst_of_starting_y.append(i * unit_block_size)
#     # # although both have the same values, this makes it easier to read
#     # for block in lst_of_unit_blocks:
#     #     if block[0].position[1] == 0: #it's a starting column
#     #         index = lst_of_starting_x.index(block[0].position[0])
#     #         # want the position of the x as we are going across the top
#     #         to_return.insert(index, [block[0].colour])
#     #         # needs to be list
#     # for block in lst_of_unit_blocks:
#     #     x_index = lst_of_starting_x.index(block[0].position[0])
#     #     y_index = lst_of_starting_y.index(block[0].position[1])
#     #     if y_index != 0:
#     #         to_return[x_index].insert(y_index, block[0].colour)
#     #         # insert at appropriate index
#     # return to_return
#
#     # while shallow_of_unit_blocks != []:
#     #     for block in lst_of_unit_blocks:
#     #         if block[1][1] == 0: # the columns coordinate
#     #             to_return.append([block[0].color])
#     #             # will form a list of the colors
#     #             shallow_of_unit_blocks.remove(block)
#
#
#
#
#         # it's children are unit cells
#
#     # else:
#     #     for sublist in block.children:
#         # lst_to_return = []
#     # ordered_lst = []
#     # if block.children != []:
#     #     first = block.children[1]
#     #     second = block.children[2]
#     #     third = block.children[0]
#     #     fourth = block.children[3]
#     #     ordered_lst.extend([first, second, third, fourth])
#     #     # orders the blocks in the correct order
#     # if block.level == block.max_depth:
#     #     lst_to_return.append(block.colour)
#     # elif block.children == []:
#     #     lst_to_return.append(block.colour)
#     # else:
#     #     for child in ordered_lst:
#     #         lst_to_return.append(_flatten(child))
#     # # will be valuable for any stack frame that has nested frames
#     # for i in range(len(lst_to_return)):
#     #     if isinstance(lst_to_return[i][0], list):
#     #         flattened = []
#     #         for sublist in lst_to_return[i]:
#     #             flattened.append(sublist[0])
#     #         lst_to_return[i] = flattened
#     #     # flattens out nested lists
#     #
#     # return lst_to_return
#
# #
# # def _list_depth(lst: Union[list[Any], Any], target_depth, depth=1) ->
# # list[ANY]:
# #
# #     >>> lst = [1,0]
# #     >>> _list_depth(lst, 1)
# #     [1, 0]
# #     >>> lst2 = [lst]
# #     >>> _list_depth(lst2, 2)
# #     [1, 0]
# #     >>> lst3 = [lst, lst]
# #     >>> _list_depth(lst3, 2)
# #     [1, 0, 1, 0]
# #
# #     if target_depth == depth:
# #         return lst
# #     else:
# #         lst2 = []
# #         for sublist in lst:
# #             lst2.extend(_list_depth(sublist, target_depth - 1))
# #         return lst2
#
#
#
#
#
#
# # def _is_perimeter(block_to_check: Block, larger_reference: Block) -> bool:
# #
# #     precondintion: block_to_check.children == []
# #
# #     x = larger_reference.position[0]
# #     y = larger_reference.position[1]
# #     to_check_x = block_to_check.position[0]
# #     to_check_y = block_to_check.position[1]
# #     if to_check_x == x:
# #         return True
# #     elif to_check_y == y:
# #         return True
# #     else:
# #         return False
# #
# # def _is_corner(block_to_check: Block, larger_reference: Block) -> bool:
#
# #     precondintion: block_to_check.children == []
# #
# #     x = larger_reference.position[0]
# #     y = larger_reference.position[1]
# #     to_check_x = block_to_check.position[0]
# #     to_check_y = block_to_check.position[1]
# #     return to_check_x == x and to_check_y == y
# """
class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

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


class PerimeterGoal(Goal):
    """ a goal type in which the goal is determined by the number of cells
    of the <colour> which are on the perimeter and the corners count
    for twice as much
        === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """ returns an integer which is the score of the board
        which is determined by the number of cells which are touching the
        perimeter, the corners count for twice as much"""
        target_color = self.colour
        if board.max_depth == 0 and board.colour == target_color:
            return 4
        board_lst = _flatten(board)
        counter = 0
        if board_lst[0][0] == target_color:
            counter += 1
        if board_lst[-1][-1] == target_color:
            counter += 1
        if board_lst[0][-1] == target_color:
            counter += 1
        if board_lst[-1][0] == target_color:
            counter += 1
        for cell in board_lst[0]: # first columns
            if cell == target_color:
                counter += 1
        for cell in board_lst[-1]:  # last column
            if cell == target_color:
                counter += 1
        for i in range(len(board_lst)):  # first row
            # don't want to include the first and last columns
            lst_to_not_include = [0, len(board_lst) - 1]
            if i not in lst_to_not_include:
                # don't want to include the first and last columns
                if board_lst[i][0] == target_color:
                    counter += 1
        for i in range(len(board_lst)): # last row
            lst_to_not_include2 = [0, len(board_lst) - 1]
            if i not in lst_to_not_include2:
                # don't want to include the first and last columns
                if board_lst[i][-1] == target_color:
                    counter += 1
        return counter


    def description(self) -> str:
        return "to get as many of the {} cells on the perimeter as possible, ' \
               'corners count for double".format(colour_name(self.colour))


class BlobGoal(Goal):
    """A goal subclass whose score is determined by the number highest number
     of consecutivly touching cells which are of the colour <colour>. Corners
      do not count at touching
    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
        """
    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """returns the score of <board> which is determined by the
        highest number of consecutivly touching cells of colour self.colour.
        Corners do not count as touching.
        """
        flattened_board = _flatten(board)
        lst_scores = []
        visited = []
        for column in flattened_board:
            col = []
            for _ in column:
                col.append(-1)
            visited.append(col)
        for i in range(len(flattened_board)):
            for j in range(len(flattened_board[i])):
                lst_scores.append(self._undiscovered_blob_size((i, j),
                                                               flattened_board,
                                                               visited))
        return max(lst_scores)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        dim = len(board) # because it's a square
        target = self.colour
        x = pos[0]
        y = pos[1]
        if x >= dim or y >= dim: # beyond dimension eqal because index len - 1
            return 0
        elif x < 0 or y < 0: # below dimension
            return 0
        if len(board) == 1: # it's a board with only a single unit:
            if visited[0][0] == -1: # [0][0] will be the target
                # otherwise it would have already returned
                return 0
            elif board[0][0] == target: # is target colour
                visited[0][0] = 1
                return 1
            else: # not target colour
                visited[0][0] = 1
                return 0
        # recursive part
        if board[x][y] != target:
            if visited[x][y] == -1:
                visited[x][y] = 0
                return 0
            else:
                # has already been visised so don't need to chnge visited
                return 0
        else: # the current position will therefre be the target
            counter = 1  # as this is the target color so at least one
            if visited[x][y] != -1:
                return 0
            else: # therefore hasn't been visited
                visited[x][y] = 1  # as this is the target
                up = self._undiscovered_blob_size((x, y + 1), board, visited)
                counter += up
                down = self._undiscovered_blob_size((x, y - 1), board, visited)
                counter += down
                right = self._undiscovered_blob_size((x + 1, y), board, visited)
                counter += right
                left = self._undiscovered_blob_size((x - 1, y), board, visited)
                counter += left
                return counter


    def description(self) -> str:
        return "have as many {} cells touching continuously as possible".format(
            colour_name(self.colour))


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })

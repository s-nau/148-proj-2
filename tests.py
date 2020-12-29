import pytest
from pytest import fixture
from block import generate_board, Block
from settings import COLOUR_LIST, BOARD_SIZE
# color list in order of [blue,red,green,yellow]
from goal import _flatten, _flatten_helper_function, Goal
from player import _get_block, Player, RandomPlayer, SmartPlayer
from typing import List, Optional, Tuple
import random

import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten
from renderer import Renderer
from settings import COLOUR_LIST


YELLOW = COLOUR_LIST[3]
BLUE = COLOUR_LIST[0]
RED = COLOUR_LIST[1]
GREEN = COLOUR_LIST[2]


def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)



@pytest.fixture
def renderer() -> Renderer:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    return Renderer(750)



# TOGETHER
@fixture
def unit_board_16X16():
    board = generate_board(2, 16)
    return board

@fixture()
def unit_board_8X8():
    board = generate_board(1, 8)
    return board
@fixture()
def unit_board4X4():
    board = generate_board(0,4)
    return board

@fixture()
def unit16X16_blue(unit_board_16X16):
    unit_board_16X16.colour = COLOUR_LIST[0]
    return unit_board_16X16
@fixture()
def unit8x8_blue(unit_board_8X8):
    unit_board_8X8.colour = COLOUR_LIST[0]
    return unit_board_8X8
@fixture()
def unit8x8_red(unit_board_8X8):
    unit_board_8X8.colour = COLOUR_LIST[1]
@fixture
def unit4X4_green(unit_board4X4):
    unit_board4X4.colour = COLOUR_LIST[2]
    return unit_board4X4
@fixture()
def unit4x4_yellow(unit_board4X4):
    unit_board4X4.colour = COLOUR_LIST[3]
    return unit_board4X4
@fixture()
def block_lowest():
    unit = generate_board(0, 1)
    return unit
@fixture()
def block_second_to_lowest(block_lowest):
    block_lowest.max_depth = 1
    return block_lowest
@fixture()
def with_chilrden16X16(unit_board_16X16, unit_board_8X8):
    unit_board_16X16.color = None
    set_children(unit_board_16X16, [None, YELLOW, GREEN,
                                    BLUE])
    print("16x16", unit_board_16X16)
    unit_board_8X8.colour = None
    set_children(unit_board_8X8, [YELLOW, RED,
                                  GREEN, BLUE])
    print("8x8", unit_board_8X8)
    unit_board_16X16.children[0] = unit_board_8X8
    print("16x16 after", unit_board_16X16)
    return unit_board_16X16
@fixture()
def fourxfour_level_0():
    block = Block((0,0), 4, COLOUR_LIST[0], 0, 2)
    return block

@fixture()
def game_board():
    random.seed(1001)
    board = generate_board(3, BOARD_SIZE)
    return board

@fixture()
def game_board2():
    random.seed(1)
    board = generate_board(5, BOARD_SIZE)
    return board

# flatten
def test_flatten_lowest(block_lowest):
    colour = block_lowest.colour
    assert _flatten(block_lowest) == [[colour]]

def test_flatten_second_to_lowest(block_second_to_lowest):
    colour = block_second_to_lowest.colour
    assert _flatten(block_second_to_lowest) == [[colour, colour], [colour, colour]]


# #col_builer
# def test_col_builder(fourxfour_level_0):
#     _lowest_units(fourxfour_level_0)
#     for i in range(3):
#         assert len(_col_builder(fourxfour_level_0, 0)) == 4


# flatten helper function
def test_flatten_helper():
    block = Block((0, 0), 2, COLOUR_LIST[0], 0 , 1)
    lst = [[0,0], [0,0]]
    _flatten_helper_function(block, lst, 0 , 0)
    assert lst ==  [[COLOUR_LIST[0], COLOUR_LIST[0]],  [COLOUR_LIST[0], COLOUR_LIST[0]]]
    block = Block((0, 0), 2, COLOUR_LIST[0], 0, 1)
    block._children_color_generator()
    block.children[0].colour = COLOUR_LIST[0]
    block.children[1].colour = COLOUR_LIST[1]
    block.children[2].colour = COLOUR_LIST[2]
    block.children[3].colour = COLOUR_LIST[3]
    lst = [[0, 0], [0, 0]]
    _flatten_helper_function(block, lst, 0 , 0)
    first = [COLOUR_LIST[1], COLOUR_LIST[2]]
    second = [COLOUR_LIST[0], COLOUR_LIST[3]]
    assert lst == [first, second]


def test_game_board(game_board, renderer):
    renderer.draw_board(_block_to_squares(game_board))
    renderer.save_to_file('game_board1.png')
    game_board.rotate(1)
    renderer.clear()
    renderer.draw_board(_block_to_squares(game_board))
    renderer.save_to_file('game_board_rotate_clockwise.png')

def test_combine_game_board(game_board, renderer):
    renderer.draw_board(_block_to_squares(game_board))
    renderer.save_to_file('game_board1.png')
    game_board.children[0].children[3].combine()
    _flatten(game_board)
    renderer.clear()
    goal = PerimeterGoal(COLOUR_LIST[0])
    goal.score(game_board)
    renderer.draw_board(_block_to_squares(game_board))
    renderer.save_to_file('game_board_rotate_combine.png')

def test_moves_game_board2(game_board2, renderer):
    goal1 = PerimeterGoal(COLOUR_LIST[1])
    goal2 = BlobGoal(COLOUR_LIST[1])
    renderer.draw_board(_block_to_squares(game_board2))
    renderer.save_to_file('game_board2_ref.png')
    assert goal1.score(game_board2) == 26
    assert goal2.score(game_board2) == 4*3 + 3*2 + 4*4 + 2 * 4**3
    lst_of_game_boards = []
    for i in range(10):
        lst_of_game_boards.append(game_board2.create_copy())
    lst_of_game_boards[0].rotate(1)
    renderer.clear()
    renderer.draw_board(_block_to_squares(lst_of_game_boards[0]))
    renderer.save_to_file("game_board_2_rotate1.png")
    assert goal1.score(lst_of_game_boards[0]) == 26
    assert goal2.score(lst_of_game_boards[0]) == 3*2 + 4 *3 + 4 ** 2 + 2 * 4 ** 3
    renderer.clear()
    lst_of_game_boards[1].rotate(3)
    renderer.draw_board(_block_to_squares(lst_of_game_boards[1]))
    renderer.save_to_file("game_board_2_rotate3.png")
    assert goal1.score(lst_of_game_boards[1]) == 26
    assert goal2.score(lst_of_game_boards[1]) == 3*2 + 4 *3 + 4 ** 2 + 2 * 4 ** 3
    renderer.clear()
    lst_of_game_boards[2].children[1].smash()
    renderer.draw_board(_block_to_squares(lst_of_game_boards[2]))
    renderer.save_to_file("game_board_2_smash.png")
    assert goal1.score(lst_of_game_boards[2]) == sum([1, 2, 1, 1, 8, 7, 7, 2, 8])
    assert goal2.score(lst_of_game_boards[2]) == 2 * 4 ** 3 + 4 + 6 + 4 ** 2 + 4 + 4
    renderer.clear()
    lst_of_game_boards[3].swap(1)
    renderer.draw_board(_block_to_squares(lst_of_game_boards[3]))
    renderer.save_to_file("game_board_2_swap1.png")
    assert goal1.score(lst_of_game_boards[3]) == sum([8,8,8,1,1,2,1,1])
    assert goal2.score(lst_of_game_boards[3]) == 4*4*4+4*4*2+4+3
    renderer.clear()
    lst_of_game_boards[4].swap(0)
    renderer.draw_board(_block_to_squares(lst_of_game_boards[4]))
    renderer.save_to_file("game_board_2_swap0.png")
    assert goal1.score(lst_of_game_boards[4]) == sum([3 , 3, 2, 4, 8, 8, 8, 4 ,2])
    assert goal2.score(lst_of_game_boards[4]) == 4 * 2 + 3 * 2 + 4 **2 + 2 * 4 ** 3
    renderer.clear()
    assert lst_of_game_boards[5].children[0].children[0].children[0].children[0].paint(COLOUR_LIST[3]) == False
    lst_of_game_boards[5].children[0].children[0].children[0].children[0].children[0].paint(
        COLOUR_LIST[3])
    renderer.draw_board(_block_to_squares(lst_of_game_boards[5]))
    renderer.save_to_file("game_board_2_paint.png")
    renderer.clear()
    lst_of_game_boards[6].children[2].children[3].children[1].children[3].combine()
    lst_of_game_boards[6].children[2].children[3].children[1].children[
        2].combine()
    renderer.draw_board(_block_to_squares(lst_of_game_boards[6]))
    renderer.save_to_file("game_board_2_combine.png")
    assert goal1.score(lst_of_game_boards[6]) == 26
    assert goal2.score(lst_of_game_boards[6]) == 4*4*4*2+4*4+4+4+3+3+4

def test_player(game_board2):
    random.seed(1)
    goal = BlobGoal(COLOUR_LIST[1])
    player = RandomPlayer(1, goal)
    player._proceed = True
    move = player.generate_move(game_board2)
    print(move)
    player2 = SmartPlayer(1, goal, 100)
    player2._proceed = True
    move2 = player2.generate_move(game_board2)
    print(move2)

def test_unit_board():
    random.seed(1)
    board = generate_board(1, BOARD_SIZE)
    goal = BlobGoal(COLOUR_LIST[1])
    player = RandomPlayer(1, goal)
    player._proceed = True
    move = player.generate_move(board)
    print(move)
    player2 = SmartPlayer(1, goal, 1)
    player2._proceed = True
    move2 = player2.generate_move(board)
    print(move2)

def test_depth_5_board(renderer):
    random.seed(1002)
    board = generate_board(5, BOARD_SIZE)
    renderer.draw_board(_block_to_squares(board))
    renderer.save_to_file('board_5_ref.png')
    renderer.clear()
    goal1 = BlobGoal(COLOUR_LIST[0]) # blue
    goal2 = BlobGoal(COLOUR_LIST[1]) # red
    player1 = RandomPlayer(1, goal1)
    player2 = RandomPlayer(2, goal2)
    player1._proceed = True
    move1 = player1.generate_move(board)
    move1_block = move1[2]
    to_do = _get_block(board, move1_block.position, move1_block.level)
    assert move1[0] == "swap" and move1[1] == 0
    assert to_do.swap(0)
    renderer.draw_board(_block_to_squares(board))
    renderer.save_to_file('board_5_move1.png')
    renderer.clear()
    afterfirst1 = goal1.score(board)
    afterfirst2 = goal2.score(board)
    player2._proceed = True
    move2 = player2.generate_move(board)
    move2_block = move2[2]
    to_do_2 = _get_block(board, move2_block.position, move2_block.level)
    assert move2[0] == "smash"
    assert to_do_2.smash()
    renderer.draw_board(_block_to_squares(board))
    renderer.save_to_file('board_5_move2.png')
    renderer.clear()
    aftersecond1 = goal1.score(board)
    aftersecond2 = goal2.score(board)
    player1._proceed = True
    move3 = player1.generate_move(board)
    move3_block = move3[2]
    to_do_3 = _get_block(board, move3_block.position, move3_block.level)
    assert move3[0] == "rotate" and move3[1] == 3
    assert to_do_3.rotate(3)
    renderer.draw_board(_block_to_squares(board))
    renderer.save_to_file('board_5_move3.png')
    renderer.clear()
    afterthird1 = goal1.score(board)
    afterthird2 = goal2.score(board)

def test_depth_5_2():
    random.seed(1002)
    board = generate_board(5, BOARD_SIZE)
    copy = board.create_copy()
    assert board == copy
    assert id(board) != id(copy)
    for i in range(len(board.children)):
        assert id(board.children[i]) != id(copy.children[i])








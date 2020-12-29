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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    goals = generate_goals(sum([num_human, num_random, len(smart_players)]))
    human_lst = []
    random_lst = []
    smart_lst = []
    for i in range(num_human):
        human_lst.append(HumanPlayer(i, goals[i]))
    id_of_last_human = 0
    if num_human > 0:
        id_of_last_human = human_lst[-1].id + 1
    for j in range(num_random):
        random_lst.append(RandomPlayer(j + id_of_last_human,
                                       goals[j + id_of_last_human]))
    id_of_last_random = id_of_last_human
    if num_random > 0:
        id_of_last_random = random_lst[-1].id + 1
    for k in range(len(smart_players)):
        smart_lst.append(SmartPlayer(k + id_of_last_random,
                                     goals[k + id_of_last_random],
                                     smart_players[k]))
    total_lst = []
    total_lst.extend(human_lst)
    total_lst.extend(random_lst)
    total_lst.extend(smart_lst)
    return total_lst

    # lst_of_humans = []
    # lst_of_random = []
    # lst_of_smart_players = []
    # lst_of_goals = generate_goals(sum([num_human, num_random,
    # len(smart_players)
    #                                    ]))
    # for i in range(num_human):
    #     lst_of_humans.append(HumanPlayer(i, lst_of_goals[i]))
    # id_of_last_human = 0
    # if len(lst_of_humans) > 0:
    #     id_of_last_human = lst_of_humans[-1].id + 1
    # for i in range(num_random):
    #     lst_of_random.append(RandomPlayer(i + id_of_last_human, lst_of_goals[
    #         i + id_of_last_human]))
    # id_of_last_random = id_of_last_human
    # if len(lst_of_random) > 0:
    #     id_of_last_random = lst_of_random[-1].id + 1
    # for i in range(len(smart_players)):
    #     lst_of_smart_players.append(SmartPlayer(i + id_of_last_random,
    #                                             lst_of_goals[
    #                                                 i + id_of_last_random],
    #                                             smart_players[i]))
    # total_players = []
    # total_players.extend(lst_of_humans)
    # total_players.extend(lst_of_random)
    # total_players.extend(lst_of_smart_players)
    # return smart_players
    # lst_human_players = []
    # lst_random_players = []
    # lst_smart_players = []
    # lst_total_players = []
    # goals = generate_goals(sum([num_human, num_random, len(smart_players)]))
    # # should return lst of goal
    # for i in range(len(goals) - len(smart_players)):
    #     if len(lst_human_players) < num_human:
    #         lst_human_players.append(HumanPlayer(i, goals[i]))
    #     elif len(lst_random_players) < num_random:
    #         lst_random_players.append(RandomPlayer(i, goals[i]))
    # if len(lst_random_players) != 0:
    #     id_of_last_random = lst_random_players[-1].id
    # elif len(lst_human_players) != 0:  # if no random players
    #     id_of_last_random = lst_human_players[-1].id
    # else:  # if no human or random players
    #     id_of_last_random = 0
    # for i in range(len(smart_players)):
    #     lst_smart_players.append(SmartPlayer(i + id_of_last_random, goals[
    #         i + id_of_last_random], smart_players[i]))
    #
    # lst_total_players.extend(lst_human_players)
    # lst_total_players.extend(lst_random_players)
    # lst_total_players.extend(lst_smart_players)
    # return lst_total_players


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """

    size = block.size
    pos = block.position
    pos_x = pos[0]
    pos_x_max = pos_x + size
    pos_y = pos[1]
    pos_y_max = pos_y + size
    loc_x = location[0]
    loc_y = location[1]
    # inside the top and left ledge which is why it's inclusive
    if block.level == level and (pos_x <= loc_x < pos_x_max) and (
            pos_y <= loc_y < pos_y_max):
        return block

    else:
        for child in block.children:
            if _get_block(child, location, level) is not None:
                return _get_block(child, location, level)
        return None

def _random_block_generator(block: Block, target_level: int) -> Block:
    """ returns a block which is randomly generated which is at level
    <target_level>
    precondiction target level and is valid for block

    >>> block1 = Block((0,0), 2, (1, 128, 181), 0, 1)
    >>> _random_block_generator(block1, 0) == block1
    True
    """

    # if target_level == 0:
    #     return block
    # elif block.children == []: # no children, but target_level not zero
    #     return block
    # else:
    #     if block.children[target_child] == target_level:
    pos_target_children = [0, 1, 2, 3]
    target_child = random.choice(pos_target_children)
    if block.level == target_level:  # block isn't always at target level
        return block
    elif block.children == []:  # has no children
        return block
    else:  # has children
        return _random_block_generator(
            block.children[target_child], target_level)


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """returns a tuple with values that are the first value in <action>, the
    second values in <action> and the Block object <block>"""
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, min(self._level, board.max_depth))

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """
    === Private Attributes ===
    _proceed:
      True when the player should make a move, False when the player should
      wait.
    === Public Attributes ===
    id:
    the id of the player
    goal:
    the goal of the player

      """
    _proceed: bool
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """initalizes RandomPlayer with the given id <player_id> and given goal
        <goal>"""
        self._proceed = False
        Player.__init__(self, player_id, goal)

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """returns None"""
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """ sets self._proceed to to true iff
        <event>.type == pygame.MOUSEBUTTONDOWN and <event>.button == 1"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        returned = False
        to_return = None  # just for pyta
        if board.max_depth == board.level:
            target_level_ops = [0]
        else:
            target_level_ops = list(range(board.max_depth - board.level))
            # not inclusive from current level until the bottom
            target_level_ops.append(target_level_ops[-1] + 1)
            # need inclusive
        while not returned:
            target_level = random.choice(target_level_ops)
            copy = board.create_copy()
            target_block = _random_block_generator(copy, target_level)
            targ2 = _get_block(board, target_block.position, target_block.level)
            copy_target = target_block.create_copy()
            move = random.choice([
                "smash", "swap", "rotate", "paint", "combine"])
            if move == "smash":
                if copy_target.smashable():
                    # it can be done, does mean it will be done
                    returned = True
                    to_return = SMASH + (targ2,)
            elif move == "swap":
                if copy_target.children != [] and copy_target.level != \
                        copy_target.max_depth:
                    # has children, otherwise can't swap
                    direction = random.choice([SWAP_VERTICAL, SWAP_HORIZONTAL])
                    returned = True
                    to_return = direction + (targ2,)
            elif move == "rotate":
                if copy_target.children != [] and copy_target.level != \
                        copy_target.max_depth:
                    direction = random.choice([ROTATE_CLOCKWISE,
                                               ROTATE_COUNTER_CLOCKWISE])
                    returned = True
                    to_return = direction + (targ2,)
            elif move == "paint":
                if copy_target.paint(self.goal.colour):
                    returned = True
                    to_return = PAINT + (targ2,)
            else: # move therefore is combine
                if copy_target.combine():
                    returned = True
                    to_return = COMBINE + (targ2,)
        self._proceed = False  # Must set to False before returning!
        return to_return

    # def _random_block_generator(self, block: Block, target_level: int)
    # -> Block:
    #     """ returns a block which is randomly generated which is at level
    #     <target_level>
    #     precondiction target level and is valid for block
    #
    #     >>> block1 = Block((0,0), 2, (1, 128, 181), 0, 1)
    #     >>> goal = generate_goals(1)
    #     >>> rand_player = RandomPlayer(1, goal)
    #     >>> rand_player._random_block_generator(block1, 0) == block1
    #     True
    #     """
    #
    #     # if target_level == 0:
    #     #     return block
    #     # elif block.children == []: # no children, but target_level not zero
    #     #     return block
    #     # else:
    #     #     if block.children[target_child] == target_level:
    #     pos_target_children = [0, 1, 2, 3]
    #     target_child = random.choice(pos_target_children)
    #     if block.level == target_level: # block isn't always at target level
    #         return block
    #     elif block.children == []: # has no children
    #         return block
    #     else: # has children
    #         return self._random_block_generator(
    #             block.children[target_child], target_level)


class SmartPlayer(Player):
    """
    === Private Attributes ===
    _proceed:
      True when the player should make a move, False when the player should
      wait.
    _difficulty:
    the difficulty level of the player
    === Public Attributes ===
    goal:
    the goal of the player
    id:
    the id of the player
      """
    _proceed: bool
    _difficulty: int
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """initalizes a SmartPlayer with id <player_id> and with goal <goal>
        and with difficulty <diffiulty>.
        precondition: diffficulty >= 1"""
        self.id = player_id
        Player.__init__(self, player_id, goal)
        self._difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """returns None"""
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """ sets self._proceed to to true iff
        <event>.type == pygame.MOUSEBUTTONDOWN and <event>.button == 1"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        n = self._difficulty  # number of moves to makes
        list_pairs_of_move_to_score = []
        # first element is a move second is a score
        lst_of_boards_and_moves = []  # list of lists
        # first element of the sublists is a board, second is a move
        lst_of_boards = []  # n boards to make sure not to mutate same boards
        for i in range(n):
            lst_of_boards.append(board.create_copy())
        for i in range(n):
            # ensures that the target block is in the board
            lst_of_boards_and_moves.append(
                [lst_of_boards[i], self._random_move_generator(
                    lst_of_boards[i])])
        for move in lst_of_boards_and_moves:  # all the possilbe moves
            # mutating_board = move[0]
            # action = move[1][0]
            # targ_block = move[1][2]
            # attempted_move = move[1]
            # num_for_rot_and_swap = move[1][1]
            if move[1][0] == "smash":
                move[1][2].smash()
                list_pairs_of_move_to_score.append([move[1],
                                                    self.goal.score(move[0])])
            elif move[1][0] == "swap":
                move[1][2].swap(move[1][1])
                list_pairs_of_move_to_score.append([move[1],
                                                    self.goal.score(move[0])])
            elif move[1][0] == "rotate":
                move[1][2].rotate(move[1][1])
                list_pairs_of_move_to_score.append([move[1],
                                                    self.goal.score(move[0])])
            elif move[1][0] == "paint":
                move[1][2].paint(self.goal.colour)
                list_pairs_of_move_to_score.append([move[1],
                                                    self.goal.score(move[0])])
            else:
                move[1][2].combine()
                list_pairs_of_move_to_score.append([move[1],
                                                    self.goal.score(move[0])])
        list_of_score_and_move = [0, self.goal.score(board)]
        for pair in list_pairs_of_move_to_score:  # greatest score
            if pair[1] > list_of_score_and_move[1]:
                list_of_score_and_move = [pair[0], pair[1]]
        self._proceed = False  # Must set to False before returning!
        if list_of_score_and_move[1] == self.goal.score(board):
            return PASS + (board,)
        else: # if score doesn't increase
            to_return_block = _get_block(board,
                                         list_of_score_and_move[0][2].position,
                                         list_of_score_and_move[0][2].level)
            to_return = (list_of_score_and_move[0][0],
                         list_of_score_and_move[0][1], to_return_block)
            return to_return

    # def _random_block_generator(self, block: Block, target_level: int) ->
    # Block:
    #     """ returns a block which is randomly generated which is at level
    #     <target_level>
    #     precondiction target level and is valid for block
    #     >>> block1 = Block((0,0), 2, (1, 128, 181), 0, 1)
    #     >>> goal = generate_goals(1)
    #     >>> rand_player = SmartPlayer(1, goal, 10000)
    #     >>> rand_player._random_block_generator(block1, 0) == block1
    #     True
    #     """
    #
    #     # if target_level == 0:
    #     #     return block
    #     # elif block.children == []: # no children, but target_level not zero
    #     #     return block
    #     # else:
    #     #     if block.children[target_child] == target_level:
    #     pos_target_children = [0, 1, 2, 3]
    #     target_child = random.choice(pos_target_children)
    #     if block.level == target_level:
    #         return block
    #     elif block.children == []:  # has no children
    #         return block
    #     else:  # has children
    #         return self._random_block_generator(
    #             block.children[target_child], target_level)

    def _random_move_generator(self, board: Block) -> [
            Tuple[str, Optional[int], Block]]:
        """ returns a randomly generated move that is a valid move for <board>
        which will apply to a randomly generated block

        >>> block1 = Block((0,0), 2, (1, 128, 181), 0, 1)
        >>> goal = generate_goals(1)
        >>> rand_player = SmartPlayer(1, goal, 10000)
        >>> rand_player._random_move_generator(block1)[2] == block1
        True
        """
        returned = False
        to_return = None # for pyta
        if board.max_depth == board.level:
            target_level_ops = [0]  # works differently for 0
        else:
            target_level_ops = list(range(board.max_depth - board.level))
            # not inclusive want from current until depth
            target_level_ops.append(target_level_ops[-1] + 1)
            # need inclusive
        while not returned:
            target_level = random.choice(target_level_ops)
            target_block = _random_block_generator(board, target_level)
            copy_target = target_block.create_copy()
            move = random.choice([
                "smash", "swap", "rotate", "paint", "combine"])
            if move == "smash":
                if target_block.smashable():
                    # it can be done.
                    returned = True
                    to_return = SMASH + (target_block,)
            elif move == "swap":
                if target_block.children != [] and target_block.level != \
                        copy_target.max_depth:
                    # has children, otherwise can't swap
                    direction = random.choice([SWAP_HORIZONTAL,
                                               SWAP_VERTICAL])
                    returned = True
                    to_return = direction + (target_block,)
            elif move == "rotate":
                if target_block.children != [] and target_block.level != \
                        target_block.max_depth:
                    direction = random.choice([ROTATE_COUNTER_CLOCKWISE,
                                               ROTATE_CLOCKWISE])
                    returned = True
                    to_return = direction + (target_block,)
            elif move == "paint":
                if copy_target.paint(self.goal.colour):
                    returned = True
                    to_return = PAINT + (target_block,)
            else:  # move therefore is combine
                if copy_target.combine():
                    returned = True
                    to_return = COMBINE + (target_block,)
        return to_return


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })

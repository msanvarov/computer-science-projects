"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Game class, which is the main class for the
Blocky game.

At the bottom of the file, there are some function that you
can call to try playing the game in several different configurations.
"""
import random
from typing import List
from block import Block, random_init
from goal import BlobGoal, PerimeterGoal
from player import Player, HumanPlayer, RandomPlayer, SmartPlayer
from renderer import Renderer, COLOUR_LIST, colour_name, BOARD_WIDTH


class Game:
    """A game of Blocky.

    === Public Attributes ===
    board:
        The Blocky board on which this game will be played.
    renderer:
        The object that is capable of drawing our Blocky board on the screen,
        and tracking user interactions with the Blocky board.
    players:
        The entities that are playing this game.

    === Representation Invariants ===
    - len(players) >= 1
    """
    board: Block
    renderer: Renderer
    players: List[Player]

    def __init__(self, max_depth: int,
                 num_human: int,
                 random_players: int,
                 smart_players: List[int]) -> None:
        """Initialize this game, as described in the Assignment 2 handout.

        Precondition:
            2 <= max_depth <= 5
        """
        # may be redundant but to keep the helper functioning, these are
        # initialized as global variables
        self.max_depth, self.num_human, self.random_players, self.smart_players\
            = max_depth, num_human, random_players, smart_players

        self.renderer = Renderer(num_human + random_players +
                                 len(smart_players))
        self.players = list()
        # runing the helper function
        self.make_players()
        self.board = random_init(0, self.max_depth)
        # just passing in a tuple of (0,0) as a starting point
        self.board.update_block_locations((0, 0), BOARD_WIDTH)
        for player_ in self.players:
            # screen should be only displayed for Human Players
            if isinstance(player_, HumanPlayer):
                self.renderer.display_goal(player_)

    def make_players(self) -> None:
        """ Helper to create Player subclass
        objects to help populate self.players. Mutates the global variable
        self.players by appending Player subclasses.
        """
        # helper is implemented to reduce Game.__init__ cluter of code
        _generated_goal = random.randint(0, 1)
        # faster than writing to cases for PerimeterGoal and BlobGoal
        if _generated_goal == 0:
            goal = PerimeterGoal
        else:
            goal = BlobGoal
        # id_ is a counter for the player_id
        id_ = 0
        # colour_ in the for loop to truly guarantee randomness
        for _ in range(self.num_human):
            colour_ = random.randint(0, len(COLOUR_LIST) - 1)
            self.players.append(
                HumanPlayer(self.renderer, id_, goal(COLOUR_LIST[colour_])))
            id_ += 1
        for _ in range(self.random_players):
            colour_ = random.randint(0, len(COLOUR_LIST) - 1)
            self.players.append(
                RandomPlayer(self.renderer, id_, goal(COLOUR_LIST[colour_])))
            id_ += 1
        for smart in range(len(self.smart_players)):
            colour_ = random.randint(0, len(COLOUR_LIST) - 1)
            self.players.append(
                SmartPlayer(self.renderer, id_, goal(COLOUR_LIST[colour_]),
                            self.smart_players[smart]))
            id_ += 1

    def run_game(self, num_turns: int) -> None:
        """Run the game for the number of turns specified.

        Each player gets <num_turns> turns. The first player in self.players
        goes first.  Before each move, print to the console whose turn it is
        and what the turn number is.  After each move, print the current score
        of the player who just moved.

        Report player numbers and turn numbers using 1-based counting.
        For example, refer to the self.players[0] as 'Player 1'.

        When the game is over, print who won to the console.

        """
        # Index within self.players of the current player.
        index = 0
        for turn in range(num_turns * len(self.players)):
            player = self.players[index]
            print(f'Player {player.id}, turn {turn}')
            if self.players[index].make_move(self.board) == 1:
                break
            else:
                print(f'Player {player.id} CURRENT SCORE: ' +
                      f'{player.goal.score(self.board)}')
                index = (index + 1) % len(self.players)

        # Determine and report the winner.
        max_score = 0
        winning_player = 0
        for i in range(len(self.players)):
            score = self.players[i].goal.score(self.board)
            print(f'Player {i} : {score}')
            if score > max_score:
                max_score = score
                winning_player = i
        print(f'WINNER is Player {winning_player}!')
        print('Players had these goals:')
        for player in self.players:
            print(f'Player {player.id} ' +
                  f'goal = \n\t{player.goal.description()}: ' +
                  f'{colour_name(player.goal.colour)}')


def auto_game() -> None:
    """Run a game with two computer players of different difficulty.
    """
    #random.seed(220)
    game = Game(1, 0, 0, [1, 6])
    game.run_game(8)


def two_player_game() -> None:
    """Run a game with two human players.
    """
    random.seed(12313)
    game = Game(4, 2, 0, [])
    game.run_game(5)


def solitaire_game() -> None:
    """Run a game with one human player.
    """
    # random.seed(507)
    game = Game(3, 1, 0, [])
    game.run_game(30)


def sample_game() -> None:
    """Run a sample game with one human player, one random player,
    and one smart player.
    """
    random.seed(1001)
    game = Game(5, 1, 1, [6])
    game.run_game(3)


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-io': ['run_game'],
    #     'allowed-import-modules': [
    #         'doctest', 'python_ta', 'random', 'typing',
    #         'block', 'goal', 'player', 'renderer'
    #     ],
    # })
    # sample_game()
    auto_game()
    #solitaire_game()
    # two_player_game()

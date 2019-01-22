"""
functions to run TOAH tours.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(delay_between_moves) in your
# solution for 'if __name__ == "main":'
import time
from toah_model import TOAHModel


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    """
    number = model.get_number_of_cheeses()
    if animate is True:
        time.sleep(delay_btw_moves)
        move_cheese(number, 0, 1, 2, 3, model, delay_btw_moves)
    else:
        move_cheese(number, 0, 1, 2, 3, model, 0)


def move_cheese3(num, source, inter, dest, model, delay_btw_moves):
    """
    Helper Function for tour_of_four_stools. This is a 3 stool algorithm
    @type num: int
    @type source: int
    @type inter: int
    @type dest: int
    @type model: TOAHModel
    @type delay_btw_moves: float
    @rtype None
    """
    if num > 1:
        move_cheese3(num - 1, source, dest, inter, model, delay_btw_moves)
        move_cheese3(1, source, inter, dest, model, delay_btw_moves)
        move_cheese3(num - 1, inter, source, dest, model, delay_btw_moves)
    else:
        model.move(source, dest)
        print(model)
        time.sleep(delay_btw_moves)


def move_cheese(num, source, inter1, inter2, dest, model, delay_btw_moves):
    """
    Helper Function for tour_of_four_stools. This is a 4 stool algorithm
    @type num: int
    @type source: int
    @type inter1: int
    @type inter2: int
    @type dest: int
    @type model: TOAHModel
    @type delay_btw_moves: float
    @rtype None
    """
    if num > 1:
        if num >= 2:
            if num >= 10:
                i = for_i(num)
            else:
                i = num - num//2
        else:
            i = 1
        move_cheese(num-i, source, inter1, dest, inter2, model, delay_btw_moves)
        move_cheese3(i, source, inter1, dest, model, delay_btw_moves)
        move_cheese(num-i, inter2, source, inter1, dest, model, delay_btw_moves)
    else:
        model.move(source, dest)
        print(model)
        time.sleep(delay_btw_moves)


def for_i(number):
    """
    Helper function to generate different values of i, if number of cheeses
    greater than or equal to 10
    @type number: int
    @rtype int
    """
    i = number//2
    if number >= 10:
        return i - i//2 + 1
    else:
        return [for_i(i) for i in range(number)]

if __name__ == '__main__':
    num_cheeses = 8
    delay_between_moves = 0.5
    console_animate = False

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)

    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)
    print("Shortest steps to solution: {}".format(four_stools.number_of_moves()))
    # Leave files below to see what python_ta checks.
    # File tour_pyta.txt must be in same folder
    # import python_ta
    # python_ta.check_all(config="tour_pyta.txt")

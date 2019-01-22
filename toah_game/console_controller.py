"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""



from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, dest):
    """ Apply move from origin to destination in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int origin:
        stool number (index from 0) of cheese to move
    @param int dest:
        stool number you want to move cheese to
    @rtype: None
    """
    TOAHModel.move(model, origin, dest)


class ConsoleController:
    """ Controller for text console.
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self:
        @param int number_of_cheeses:
        @param int number_of_stools:
        @rtype: None
        """
        self.number_of_cheeses = number_of_cheeses
        self.number_of_stools = number_of_stools

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self:
        @rtype: None

        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        """
        game = TOAHModel(self.number_of_stools)
        game.fill_first_stool(self.number_of_cheeses)
        print("~~~~~~~~~~WELCOME TO FAIYAZ AND RASU'S GAME~~~~~~~~~~\n")
        print("~~~~~~~~~~OBJECTIVES~~~~~~~~~~")
        print("To Move the entire stack of cheese from one stool to another stool\n")
        print("~~~~~~~~~~INSTRUCTIONS~~~~~~~~~~")
        print("1. Move cheese from one stool to another one at a time \n"
              "2. Can only move the top most cheese from a stool \n"
              "3. Can't place a larger cheese over a smaller cheese \n"
              "4. To exit the game, enter 'exit'")
        print('START \n \n ')
        print(game)
        start = 'Open'
        while start != 'exit':
            origin = int(input("Enter the stool from which you want to move the cheese. "
                    + "Stools range from 0 to " + str(self.number_of_stools -1) + ': '))
            final = int(input("Now enter the stool you want to "
                        "move the slice of cheese to. Stools range from 0 to " + str(self.number_of_stools -1 ) + '\n'))
            try:
                move(game, origin, final)
            except IllegalMoveError as error:
                print("!!!!!!You caused an error!!!!!!!")
                print(error)

            print(game)
            start = input("type 'exit' to exit")

if __name__ == '__main__':
    # TODO: Press Numlock
    stool = int(input(
        "Enter the number of stools you would want to play the game with: "))
    if stool <= 0:
        while stool <= 0:
            print('Number of stools have to be greater than 0')
            stool = int(input('Enter again: '))
    model = TOAHModel(stool)
    cheese = int(input(
        "Now, enter the number of cheeses you would want to play the game with: "))
    if cheese <= 0:
        while cheese <= 0:
            print('Number of cheeses have to be greater than 0')
            cheese = int(input('Enter again: '))
    c = ConsoleController(cheese, stool)
    c.play_loop()
    import python_ta
    python_ta.check_all(config="consolecontroller_pyta.txt")

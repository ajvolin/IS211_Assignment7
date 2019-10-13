#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pig.py: IS 211 Assignment 7."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

# Imports
import sys
import argparse
import random
from queue import Queue


class Players(object):
    """This class is used to track the players for a game of Pig.

    The attributes of this class are private as they should not
    be accessed or set directly. This is ensures the integrity
    of the game.

    Attributes:
        __players (Queue): The players queue.
        __current_player (Player): The currently dequeued player.
    """

    def __init__(self, players):
        """ 
        The constructor for Players class. 

        Parameters: 
            players (Queue): The queue holding the players. 
        """
        self.__players = players
        self.__current_player = players.get()

    def get_current_player(self):
        """ 
        The getter for the __current_player attribute.

        Returns:
            (Player): The current player.
        """
        # Return the current player
        return self.__current_player

    def get_next_player(self):
        """ 
        A method to get the next player in the Players queue.

        Returns:
            (Player): The current player.
        """
        # Add current player back to the end of the queue
        self.__players.put(self.__current_player)
        # Get the next player from the queue and return it
        self.__current_player = self.__players.get()
        return self.__current_player

    def get_players(self):
        """ 
        The getter for the __players attribute.

        Returns:
            (Queue): The players queue.
        """
        # Add current player back to the queue before returning the players
        self.__players.put(self.__current_player)
        return self.__players


class Player(object):
    """This class is used to store details about a player.

    The attributes of this class are private as they should not
    be accessed or set directly. This is ensures the integrity
    of the game.

    Attributes:
        __name (str): The player's name.
        __score (int): The player's total score.
        __rolls (int): The player's number of rolls.
    """

    def __init__(self, name):
        """ 
        The constructor for Player class. 

        Parameters: 
            name (string): The player's name.
        """
        self.__name = name.strip()
        self.__score = 0
        self.__rolls = 0

    def get_name(self):
        """ 
        The getter for the __name attribute.

        Returns:
            (strings): The player's name.
        """
        # Return the player's name
        return self.__name

    def get_score(self):
        """ 
        The getter for the __score attribute.

        Returns:
            (int): The player's total score.
        """
        # Return the player's score
        return self.__score

    def get_rolls(self):
        """ 
        The getter for the __rolls attribute.

        Returns:
            (int): The player's number of rolls.
        """
        # Return the player's rolls
        return self.__rolls

    def commit_score(self, score, rolls):
        """ 
        Method to increment the __score and __rolls attributes.

        Parameters: 
            score (int): The player's score from their last turn.
            rolls (int): The player's number of rolls from their last turn.
        """
        # Update the player's score and roll count
        self.__score += score
        self.__rolls += rolls


class Die(object):
    """This class is used to generate a die for a game."""

    def __init__(self):
        """ 
        The constructor for Player class. 

        Seeds the random generator with 0,
        """
        # Set the seed to 0
        random.seed(0)

    def roll(self):
        """ 
        Method to 'roll' the die.

        Returns:
            (int): The result of the 'roll', an integer between 1 and 6
        """
        # Return a random integer between 1 and 6
        return random.randint(1, 6)


class Game(object):
    """This class is used to run a game of Pig.

    The attributes of this class are private as they should not
    be accessed or set directly. Additionally, most functions of
    this class are private to prevent manipulation of the game.
    This is ensures the integrity of the game.

    Attributes:
        __players (Players): The instantiated players for this game.
        __die (Die): The die instantiated for this game.
    """

    def __init__(self, players):
        """ 
        The constructor for Game class.

        Instantiates the players and die for the current game.

        Parameters: 
            players (Queue): The players queue for the current game.
        """
        # Instantiate a Players object with the players queue
        self.__players = Players(players)
        # Instantiate the Die to be used for the current game
        self.__die = Die()

    def start(self):
        """The method to start the current game."""
        # Call the private __turn method to start the game
        self.__turn()

    def __game_over(self):
        """
            The method to run at the end of the current game.

            Prints a leaderboard with the scores and number of
            rolls for each of the current game's players.
        """
        # Get the players and create the leaderboard tuple
        leaderboard = ((player.get_name(), player.get_score(), player.get_rolls())
                       for player in list(self.__players.get_players().queue))

        print("\nLEADERBOARD\n")
        # Print leaderboard header border
        print("+-{:<32}-+-{:>10}-+-{:>10}-+".format("-"*32, "-"*10, "-"*10))
        # Print the leaderboard header
        print("| {:<32} | {:>10} | {:>10} |".format(
            'Player', 'Score', '# of Rolls'))
        # Sort by highest scores first and print the details
        for player in sorted(leaderboard,
                             key=lambda player: (player[1]),
                             reverse=True):
            # Print the cell separators
            print("|-{:<32}-+-{:>10}-+-{:>10}-|".format("-"*32, "-"*10, "-"*10))
            # Print the player's details
            print("| {:<32} | {:>10} | {:>10} |".format(
                player[0], player[1], player[2]))

        # Print leaderboard footer border
        print("+-{:<32}-+-{:>10}-+-{:>10}-+".format("-"*32, "-"*10, "-"*10))

    def __turn(self, next_player=False):
        """
        The method to control a player's turn.

        Parameters: 
            next_player (bool): Used to decide if the next player
                                should be called to play. Defaults
                                to False.
        """
        # Get the player for the current turn
        player = self.__players.get_current_player(
        ) if not next_player else self.__players.get_next_player()
        # Keep track of the current score and rolls
        current_score = 0
        rolls = 0
        # Keep track of the turn and game status
        active_turn = True
        game_over = False
        # Let the players know who's turn it is
        print("\n{}, it's your turn. Your current score is {}".format(
            player.get_name(), player.get_score()))

        # Keep the current player's turn until they roll a 1,
        # win the game, or hold.
        while active_turn and not game_over:
            # Request the current player's desired action
            action = input(
                "Enter 'r' to roll the die, or 'h' to hold. What you you like to do? ")

            # Player chose to roll
            if action == "r":
                # Roll the die and add to roll total for the turn
                roll = self.__die.roll()
                rolls += 1
                # If the player rolls 1, reset the current
                # score and commit the current rolls count
                # to the player's Player object, and exit
                # the loop.
                if roll == 1:
                    current_score = 0
                    player.commit_score(current_score, rolls)
                    print("Ouch, {} you rolled a {} and lost all points you accumulated during this turn. Your score for this turn is {}. Your total score is {}.".format(
                        player.get_name(), roll, current_score, player.get_score()))
                    active_turn = False
                # If the player rolled other than a 1, update the
                # current score to the value of the roll, check
                # to see if the player's total is >= 100 and end
                # the game, otherwise ask the player for their
                # next action
                else:
                    current_score += roll
                    if (current_score + player.get_score()) >= 100:
                        player.commit_score(current_score, rolls)
                        print("\n\nCongratulations {}, you rolled a {} and your total score is {}. You won the game!"
                              .format(player.get_name(), roll, player.get_score()))
                        game_over, active_turn = True, False
                    else:
                        print("Nice {}! You rolled a {}. Your current score for this turn is {}. Your total score is {}".format(
                            player.get_name(),
                            roll,
                            current_score,
                            current_score + player.get_score()
                        )
                        )
            # Player chose to hold, commit their current score and
            # roll count to their Player object and exit the loop
            elif action == "h":
                player.commit_score(current_score, rolls)
                print("{}, you held. Your score for this turn is {}. Your total score is {}.".format(
                    player.get_name(), current_score, player.get_score()))
                active_turn = False
            # The player entered an invalid action
            else:
                print("You entered an invalid action.")

        # Check to see if the game is over, if not go to the next player,
        # otherwise call the private __game_over function to trigger the
        # leaderboard display
        if not game_over:
            self.__turn(True)
        else:
            self.__game_over()


def main():
    """The method that runs when the program is executed."""

    # Setup --numPlayer argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--numPlayers',
                        help='The number of players for the game.',
                        type=int
                        )
    args = parser.parse_args()

    # Check for the numPlayers argument
    player_count = args.numPlayers if args.numPlayers else 2

    # Check to see if there are less than two players
    if player_count < 2:
        print("You entered an invalid number of players. At least two players are required to play this game. Please try again.")
        sys.exit()

    # Create a queue for the players
    players = Queue()

    # Setup Player objects for each player and put them in the players Queue
    for i in range(0, player_count):
        # Request the player's name
        player = Player(input("What is Player {}'s name? "
                              .format(str(i+1))))
        # Add the player to the players queue
        players.put(player)

    # Start the game, passing the players queue to the Game class
    Game(players).start()

    # Exit the program after the game is over
    sys.exit()


if __name__ == '__main__':
    main()

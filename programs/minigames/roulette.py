import random
from typing import override

from managers.gambling_manager import GamblingManager
from programs.abstract_program import AbstractProgram


class RouletteMinigame(AbstractProgram):
    """
    A simple roulette minigame.

    Written by Parker Cornelius. Adapted to the AbstractProgram interface by Daniel Myers.
    """

    def __init__(self, gambling_manager: GamblingManager):
        super().__init__()
        self.__gambling_manager = gambling_manager
        self.__wheel = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 0, "00"]
        self.__money_pool = None
        self.__bet_type = None

    @override
    def _execute(self) -> bool:
        print("Roulette!")
        print("Place bets on a color or on numbers to win money based off the odds")
        print(f"Current money: {self.__gambling_manager.get_player_coins()} coins")
        print("Enter your bet: ", end="")
        return False

    @override
    def _process_input(self, user_input: str) -> bool:
        # If a bet has not yet been cast, interpret input as bet
        if self.__money_pool is None:
            successful_bet = self.__place_user_bet(user_input)
            if successful_bet:
                print("Do you want to bet on a 'number' or 'color'? ", end='')
            return False

        # If bet type has not been set, set bet type
        if self.__bet_type is None:
            user_input = user_input.lower()
            if user_input == 'number':
                self.__bet_type = 'number'
                print("Enter bet numbers (comma seperated): ", end='')
                return False
            elif user_input == 'color':
                self.__bet_type = 'color'
                print("Enter a color ('red', 'black', or 'green') ", end='')
                return False
            else:
                print("Chose 'number' or 'color'")
                print("Do you want to bet on a 'number' or 'color'? ", end='')
                return False

        # Gather input for specific bet type and then run roulette.
        if self.__bet_type == 'number':
            try:
                bet_numbers = [int(x.strip()) for x in user_input.split(',')]
            except ValueError:
                print("Invalid bet. Try again: ", end='')
                return False
        elif self.__bet_type == 'color':
            bet_numbers = []
            user_input = user_input.lower()
            if user_input in ['red', 'black', 'green']:
                bet_color = user_input
            else:
                print("Please enter 'red', 'black', or 'green'.")
                return False

        # Spin the wheel
        result = random.choice(self.__wheel)
        if result in [0, "00"]:
            result_color = 'green'
        elif result % 2 == 1:
            result_color = 'red'
        else:
            result_color = 'black'
        print(f"\nThe wheel landed on: {result} ({result_color})")

        # Calculate winnings
        winnings = 0

        # number betting results
        if self.__bet_type == 'number':
            if result in bet_numbers:
                payout_odds = (len(bet_numbers) / 38)
                winnings = round(bet - (bet * (payout_odds)))
                print(f"Congratulations! You won {winnings} coins on number {result}.")
            else:
                print(f"L, {result}")

        # Color betting results
        elif self.__bet_type == 'color':
            if bet_color == result_color:
                if bet_color == 'red' or bet_color == 'black':
                    winnings = self.__money_pool
                    print(f"Congratulations! You won {winnings} coins on {result_color}.")
                elif bet_color == 'green':
                    winnings = round(bet * 36)
            else:
                print(f"L, {result_color}")

        # Provide winnings to player
        if winnings > 0:
            self.__gambling_manager.give_player_payout(winnings)
        else:
            print(f"Lost {self.__money_pool} coins.\n")
        return True

    def __place_user_bet(self, user_input: str) -> bool:
        """Attempts to place a bet from the given user_input. Returns true if successful."""
        try:
            attempted_bet = int(user_input)
            bet_successful = self.__gambling_manager.place_gamble(attempted_bet)
            if bet_successful:
                self.__money_pool = attempted_bet
                print(f"Bet {self.__money_pool} coins!")
                return True
            else:
                print(f"Please enter a valid bet. You have {self.__gambling_manager.get_player_coins()} coins: ")
                return False
        except ValueError:
            print("Please enter a valid integer of how much to gamble: ", end='')
            return False

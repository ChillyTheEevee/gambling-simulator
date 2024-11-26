import random
from typing import override

from managers.gambling_manager import GamblingManager
from programs.abstract_program import AbstractProgram


class SlotsMinigame(AbstractProgram):
    """
    A simple slot machine minigame. I do not understand the implementation of this minigame even a little.

    Written by Caleb Arnold. "Adapted" to the AbstractProgram interface by Daniel Myers.
    """

    def __init__(self, gambling_manager: GamblingManager):
        super().__init__()
        self.__gambling_manager: GamblingManager = gambling_manager

    @override
    def _execute(self) -> bool:
        print("Welcome to slots!")
        print(f'You currently have {self.__gambling_manager.get_player_coins()} coins.')
        print('Enter the number of coins to bet, or enter stop to leave: ', end='')
        return False

    @override
    def _process_input(self, user_input: str) -> bool:
        # Exit the program if input is stop
        if user_input == 'stop':
            print("OK, Goodbye")
            return True

        # Otherwise, attempt to place bet with input
        try:
            attempted_bet = int(user_input)
            if self.__gambling_manager.is_valid_gambling_amount(attempted_bet):
                bet = attempted_bet
                self.__gambling_manager.place_gamble(bet)
            else:
                print("Please enter a valid bet: ")
                return False
        except ValueError:
            print("Please enter a valid bet: ")
            return False

        # Gamble slot
        slots = self.__run_slots()
        self.__print_slots(slots[1], slots[3], slots[5])
        info = self.__reoccur(slots[0], slots[1], slots[2], slots[3], slots[4], slots[5])
        winnings = self.__points(info[0], info[1], float(bet))
        self.__gambling_manager.give_player_payout(winnings)
        print(f'You currently have {self.__gambling_manager.get_player_coins()} coins.')
        print('Enter the number of coins to bet, or enter stop to leave: ', end='')

    def __run_slots(self):  # this function returns the random values and symbols to be used
        """Returns a tuple of random variables along with their corresponding symbols."""
        spaces = {0: '   7   ', 1: '  \N{cherries}  ', 2: '  \N{cherries}  ', 3: '  \N{lemon}  ',
                  4: '  \N{lemon}  ', 5: '  \N{watermelon}  ', 6: '  \N{watermelon}  ', 7: '  \N{banana}  ',
                  8: '  \N{banana}  ',
                  9: '  \N{gem stone}  ', 10: '  \N{gem stone}  ', 11: '  \N{bell}  ', 12: '  \N{bell}  ',
                  13: '  BAR  ',
                  14: '  BAR  ', 15: '  \N{skull}  ', 16: '  \N{skull}  ', 17: '  \N{skull}  ', 18: '  \N{skull}  ',
                  19: '  \N{skull}  ',
                  20: '  \N{skull}  '}
        # we use the \N to access the unicode, and we will use the numbers along with a random number selector to
        # access the dictionary

        sym1 = random.randint(0, 20)
        sym2 = random.randint(0, 20)
        sym3 = random.randint(0, 20)
        return sym1, spaces[sym1], sym2, spaces[sym2], sym3, spaces[sym3]

    def __print_slots(self, sym1, sym2, sym3):  # this will be used to print the slot grid
        print()
        lines = 23
        spec = ['  BAR  ', '   7   ']  # these will be used since the spacing between emojis and text diff
        if sym1 in spec and sym2 in spec and sym3 in spec:
            lines += 2  # this adjusts grid size if all are spec
        elif (sym1 in spec and sym2 in spec or sym1 in spec and sym3 in spec or sym2 in spec and
              sym3 in spec):  # this test for if 2 values are spec, and adjusts the size of the grid
            lines += 1
        print('         SLOTS         ')
        print('-' * lines)
        print('|' + sym1 + '|' + sym2 + '|' + sym3 + '|')
        print('-' * lines)
        print()

    def __reoccur(self, val1, sym1, val2, sym2, val3, sym3):
        # this function goes thru each point, counts the amount the top value reoccurs, and returns the reoccuring value, and
        # the amount it reoocurs
        value = 22
        count = 0
        if sym1 == sym2 or sym1 == sym3:
            value = val1
            count += 1
        if sym2 == sym3:
            value = val2
            count += 1
        return value, count

    def __points(self, value, count, bank):
        fruits = [1, 2, 3, 4, 5, 6, 7, 8]  # we are attaching the numbers to lists to assign certain point values
        luck = [9, 10, 11, 12, 13, 14]
        death = [15, 16, 17, 18, 19, 20]
        if value in fruits:
            if count == 1:
                bank *= 1.5
                print('2 fruits! bet x 1.5!')
            elif count == 2:
                bank *= 2
                print('3 fruit! bet x 2!')
        elif value in luck:
            if count == 1:
                bank *= 1.75
                print('2 luck points! bet x 1.7')
            elif count == 2:
                bank *= 2.5
                print('3 luck points! bet x 2.5')
        elif value in death:
            if count == 1:
                bank *= 1.5
                print('2 skulls! bet x 1.5. Close call...')
            if count == 2:
                bank = 0
                print('UNLUCKY, BET DOWN TO 0')
        elif value == 0:
            if count == 1:
                bank *= 1.5
                print('2 sevens! bet x 1.5. So close...')
            if count == 2:
                bank *= 10
                print("TRIPLE 7's!!! BET x 10!!! CONGRATS")
        elif count == 0:
            bank /= 2
            print('No matches, bet value / 2')
        return round(bank)
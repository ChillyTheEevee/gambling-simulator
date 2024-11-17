import random
from typing import override

from programs.abstract_program import AbstractProgram

cards = {
    "ace": 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    "jack": 10,
    "queen": 10,
    "king": 10,
}


class BlackjackMinigame(AbstractProgram):
    """
    A simple blackjack minigame.

    Written by Aiden Kline. Adapted to the AbstractProgram interface by Daniel Myers.
    """

    def __init__(self):
        super().__init__()
        self.__dealer_cards = None
        self.__user_cards = None

        self.__gameBegun = False

    @override
    def _execute(self) -> bool:
        print("Welcome to Blackjack!")
        print("How much would you like to gamble (integer)?: ")
        return False

    @override
    def _process_input(self, user_input: str) -> bool:
        if not self.__gameBegun:
            try:
                self.__money_pool = int(user_input)
                print(f"Bet {self.__money_pool} coins!")
            except ValueError:
                print("Please enter a valid integer of how much to gamble: ", end='')
                return False

            self._setup_game()

            player_blackjack = self._calculate_score(self.__user_cards) == 21
            dealer_blackjack = self._calculate_score(self.__dealer_cards) == 21
            if player_blackjack or dealer_blackjack:
                self._process_blackjacks(player_blackjack, dealer_blackjack)
                return True

            self._print_game_state()
            print("\nDo you want to hit, or stand?: ", end='')
            return False

        user_input = user_input.lower()
        if user_input != "hit" or "stand":
            print("Invalid input. Try again: ", end='')
            return False

        if user_input == "hit":
            drawn_card = self._generate_random_card()
            print(f"Drew a {drawn_card}!")
            self.__user_cards.append(drawn_card)
            user_score = self._calculate_score(self.__user_cards)
            print("Your current score is: " + str(user_score))
            if user_score > 21:
                print("\nBust! Better luck next time.")
                # todo implement bust endgame
                return True
            elif user_score == 21:
                print("\nAchieved a 21!")
                self._process_endgame()
                return True
            else:
                print("\nDo you want to hit, or stand?: ", end='')
                return False
        elif user_input == "stand":
            self._process_endgame()
            return True

    def _print_game_state(self) -> None:
        print(f"The dealer's shown card is: {self.__dealer_cards[0]}\n")
        print(f"Your cards are: ", end="")
        for i in range(len(self.__user_cards) - 1):
            print(self.__user_cards[i], end=", ")
        print(self.__user_cards[len(self.__user_cards) - 1])
        print("Your current score is: " + str(self._calculate_score(self.__user_cards)))

    def _calculate_score(self, cards):
        """Calculates the highest blackjack score for the cards without going over 21."""
        score = 0

        # Count non-ace score and count aces
        num_aces = 0
        for card in cards:
            if card == "ace":
                num_aces += 1
                continue
            score += cards[card]

        # Count aces to get the closest score to 21 without going over
        score += num_aces * 10
        while num_aces > 0 and score > 21:
            score -= 9
            num_aces -= 1
        return score

    def _generate_random_card(self) -> str:
        """Generates a random card type (i.e. 1, 2, 3, ..., queen, king, ace)"""
        return random.choice(list(cards.keys()))

    def _process_endgame(self) -> None:
        current_dealer_score = self._calculate_score(self.__dealer_cards)

        # The dealer will continue to draw cards until their total is above 16, or they bust
        while current_dealer_score < 17:
            # The dealer draws
            print("\nThe dealer hits again.")
            drawn_card = self._generate_random_card()
            print(f"\nThe dealer drew a {drawn_card}!")
            self.__dealer_cards.append(drawn_card)

            # Print the dealer's current cards
            print(f"The dealer's cards are: ", end="")
            for i in range(len(self.__user_cards) - 1):
                print(self.__dealer_cards[i], end=", ")
            print(self.__dealer_cards[len(self.__dealer_cards) - 1])

            # Process the dealer's score
            current_dealer_score = self._calculate_score(self.__dealer_cards)

            if current_dealer_score > 21:  # The dealer busts
                pass # todo handle dealer busts

        # The dealer has finished hitting and has not bust. Determine victor.
        # todo grant awards for victory
        user_score = self._calculate_score(self.__user_cards)
        print(f"\nThe dealer's total is: {current_dealer_score}")
        if user_score > current_dealer_score:
            print("You win! you beat the dealer.")
        else:
            print("You lose, the dealer beat you :(")



    def _setup_game(self):
        print("Dealing out cards...")
        self.__dealer_cards = [self._generate_random_card(), self._generate_random_card()]
        self.__user_cards = [self._generate_random_card(), self._generate_random_card()]
        self.__gameBegun = True

    def _process_blackjacks(self, player_blackjack: bool, dealer_blackjack: bool) -> None:
        pass  # todo implement blackjack logic
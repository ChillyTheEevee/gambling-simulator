import random
from typing import override

from managers.gambling_manager import GamblingManager
from programs.abstract_program import AbstractProgram

card_value_map = {
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

    def __init__(self, gambling_manager: GamblingManager):
        super().__init__()
        self.__gambling_manager = gambling_manager

        self.__dealer_cards = None
        self.__user_cards = None
        self.__game_begun = False

    @override
    def _execute(self) -> bool:
        print("Welcome to Blackjack!")
        print(f"You have {self.__gambling_manager.get_player_coins()} coins.")
        print("How much would you like to gamble (integer)?: ", end='')
        return False

    @override
    def _process_input(self, user_input: str) -> bool:
        if not self.__game_begun:
            # If the game has not started, prompt the user for a bet
            successful_bet = self.__place_user_bet(user_input)
            if not successful_bet:
                return False

            # If bet was successful, deal cards
            self.__game_begun = True
            print("Dealing out cards...\n")
            self.__deal_cards()
            self._print_game_state()

            # Process blackjacks
            player_blackjack = self.__calculate_score(self.__user_cards) == 21
            dealer_blackjack = self.__calculate_score(self.__dealer_cards) == 21
            if player_blackjack or dealer_blackjack:
                self.__process_blackjacks(player_blackjack, dealer_blackjack)
                return True

            # Prompt additional input if no blackjacks
            print("\nDo you want to hit, or stand?: ", end='')
            return False

        # Process hit or stand
        user_input = user_input.lower()
        if user_input != "hit" and user_input != "stand":
            print("Invalid input. Try again: ", end='')
            return False

        if user_input == "hit":
            game_over = self.__process_hit()
            return game_over
        elif user_input == "stand":
            self.__process_stand()
            return True

    def __place_user_bet(self, user_input: str) -> bool:
        """Attempts to place a bet from the given user_input. Returns true if successful."""
        try:
            attempted_bet = int(user_input)
            bet_successful = self.__gambling_manager.place_gamble(attempted_bet)
            if bet_successful:
                print(f"Bet {self.__money_pool} coins!")
                return True
            else:
                print(f"Please enter a valid bet. You have {self.__gambling_manager.get_player_coins()} coins: ")
                return False
        except ValueError:
            print("Please enter a valid integer of how much to gamble: ", end='')
            return False

    def __process_hit(self) -> bool:
        """Processes a hit. Returns true if the game ends as a result of this hit."""
        drawn_card = self.__generate_random_card()
        print(f"Drew a {drawn_card}!\n")
        self.__user_cards.append(drawn_card)
        user_score = self.__calculate_score(self.__user_cards)
        self._print_game_state()
        if user_score > 21:
            print("\nBust! Better luck next time.")
            return True
        elif user_score == 21:
            print("\nAchieved a 21!")
            self.__process_stand()
            return True
        else:
            print("\nDo you want to hit, or stand?: ", end='')
            return False

    def _print_game_state(self) -> None:
        """Prints all information available to the player when deciding to hit or stand."""
        print(f"The dealer's shown card is: {self.__dealer_cards[0]}\n")
        print(f"Your cards are: ", end="")
        for i in range(len(self.__user_cards) - 1):
            print(self.__user_cards[i], end=", ")
        print(self.__user_cards[len(self.__user_cards) - 1])
        print("Your current score is: " + str(self.__calculate_score(self.__user_cards)))

    def __print_dealer_cards(self) -> None:
        """Prints the dealer's cards. Used when the dealer is drawing."""
        print(f"The dealer's cards are: ", end="")
        for i in range(len(self.__dealer_cards) - 1):
            print(self.__dealer_cards[i], end=", ")
        print(self.__dealer_cards[len(self.__dealer_cards) - 1])

    def __calculate_score(self, cards: list[str]):
        """Calculates the highest blackjack score for cards without going over 21."""
        score = 0

        # Count non-ace score and count aces
        num_aces = 0
        for card in cards:
            if card == "ace":
                num_aces += 1
                continue
            score += card_value_map[card]

        # Count aces to get the closest score to 21 without going over
        score += num_aces * 11
        while num_aces > 0 and score > 21:
            score -= 10
            num_aces -= 1
        return score

    def __generate_random_card(self) -> str:
        """Generates a random card type (i.e. 1, 2, 3, ..., queen, king, ace)"""
        return random.choice(list(card_value_map.keys()))

    def __process_stand(self) -> None:
        """
        Processes a stand. This method allows the dealer to draw and then determines the winner
        and distributes rewards.
        """
        # The dealer reveals his card
        print(f"\nThe dealer reveals his second card, a(n) {self.__dealer_cards[1]}.")
        self.__print_dealer_cards()

        # Allow the dealer to make moves
        current_dealer_score = self.__calculate_score(self.__dealer_cards)

        # The dealer will continue to draw cards until their total is above 16, or they bust
        while current_dealer_score < 17:
            # The dealer draws
            print("The dealer hits again.")
            drawn_card = self.__generate_random_card()
            print(f"The dealer drew a {drawn_card}!")
            self.__dealer_cards.append(drawn_card)

            self.__print_dealer_cards()

            # Process the dealer's score
            current_dealer_score = self.__calculate_score(self.__dealer_cards)
        print("The dealer stands.")

        # The dealer has finished hitting. Determine victor.
        player_victory = False
        user_score = self.__calculate_score(self.__user_cards)
        print(f"\nThe dealer's total is: {current_dealer_score}")
        print(f"Your total is: {user_score}")
        if current_dealer_score > 21:
            print("The dealer busted! You win.")
            player_victory = True
        elif user_score > current_dealer_score:
            print("You win!")
            player_victory = True
        elif user_score < current_dealer_score:
            print("You lose, the dealer beat you :(")
            player_victory = False
        else:
            print("Draw! Your coins will be returned.")
            # Return the player's original bet
            self.__gambling_manager.give_player_payout(self.__money_pool)
            return

        # Distribute rewards to winner
        if player_victory:
            self.__gambling_manager.give_player_payout(self.__money_pool * 2)

    def __deal_cards(self):
        self.__dealer_cards = [self.__generate_random_card(), self.__generate_random_card()]
        self.__user_cards = [self.__generate_random_card(), self.__generate_random_card()]

    def __process_blackjacks(self, player_blackjack: bool, dealer_blackjack: bool) -> None:
        if player_blackjack:
            print("You have a blackjack!")
        print(f"The dealer reveals his second card, a(n) {self.__dealer_cards[1]}.")
        self.__print_dealer_cards()
        if dealer_blackjack:
            print("The dealer has a blackjack!")

        if player_blackjack and dealer_blackjack:
            print("Because both the player and dealer have a blackjack, it's a tie. Coins are returned.")
        elif player_blackjack:
            print("You win by blackjack! Congratulations!")
            self.__gambling_manager.give_player_payout(self.__money_pool * 3)
        elif dealer_blackjack:
            print("The dealer has a blackjack. The game is over.")

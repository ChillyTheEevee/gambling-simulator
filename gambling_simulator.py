import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, override
from typing import cast


class AbstractProgram(ABC):
    """
    An abstract representation of a terminal program.

    AbstractPrograms are processed first with an initial call to execute_program(self) and then (if necessary) with
    sequential calls to the process_user_input(self, user_input) method. When either method is called, an
    AbstractProgram will perform all tasks up until it requires additional input from a user. Then, the driver method
    will return and the AbstractProgram will wait until process_user_input(self, user_input) is called with the
    additional input required.

    An AbstractProgram retrains its state throughout sequential calls of its methods.

    The lifecycle of an AbstractProgram is as follows:
    1). Instantiation - The AbstractProgram instantiation has been instantiated, but has not yet been called.
    2). Execution - The AbstractProgram's execute_program(self) method is called and the AbstractProgram begins
            execution. This method either returns True or False.
    3). Subsequent Calls - If False is returned from execute_program(self), the AbstractProgram requires additional
            user input to complete execution and may be continued with subsequent calls to
            process_user_input(self, user_input) until process_user_input(self, user_input) returns True.
    4). Program completion - Once either a call to execute_program(self) or process_user_input(self, user_input) returns
            True, any subsequent calls to this AbstractProgram will result in an error being thrown.
    """

    def __init__(self):
        self.execution_begun = False
        self.completed_execution = False

    def execute_program(self) -> bool:
        """
        Executes this AbstractProgram until either it has reached full completion or requires additional input. This
        method ensures state checks are consistent across implementations.

        Returns:
            bool: True if this AbstractProgram has completed execution without the need for additional input,
                False otherwise.

        Exceptions:
            AlreadyExecutedException: If this AbstractProgram has already been executed.
        """
        if self.execution_begun:
            raise AlreadyExecutedException()
        self.execution_begun = True
        completion_state = self._execute()
        self.completed_execution = completion_state
        return completion_state

    @abstractmethod
    def _execute(self) -> bool:
        """
        Subclasses must implement this method to provide specific execution logic.

        Returns:
            bool: True if this AbstractProgram has completed execution without the need for additional input,
                False otherwise.
        """
        pass

    def process_user_input(self, user_input: str) -> bool:
        """
        Continues execution of this AbstractProgram until either it has reached completion or requires additional input.

        Args:
            user_input (str): The user input

        Returns:
            bool: True if the AbstractProgram has completed execution without the need for additional input,
                False otherwise.

        Exceptions:
            AbstractProgramCompleteException: If called when this AbstractProgram has already completed execution.
            ExecutionNotInitiatedException: If called when execute_program(self) has not yet been called.
        """
        if self.completed_execution:
            raise AbstractProgramCompleteException()
        if not self.execution_begun:
            raise ExecutionNotInitiatedException()
        completion_state = self._process_input(user_input)
        self.completed_execution = completion_state
        return completion_state

    @abstractmethod
    def _process_input(self, user_input: str) -> bool:
        """
        Subclasses must implement this method to handle specific execution logic.

        Returns:
            bool: True if the AbstractProgram has completed execution without the need for additional input,
                False otherwise.
        """
        pass


class AbstractItem(ABC):
    """
    An AbstractItem is an Item that a name, price, purchase message, and a picture that can be displayed.

    The __str__ method of an AbstractItem returns the picture of the Item in string form.
    """

    def __init__(self, name: str, price: int, purchase_message: str, picture: tuple[str, ...]):
        self.__name: str = name
        self.__price: int = price
        self.__picture: tuple[str, ...] = picture
        self.__purchase_message: str = purchase_message

    def get_name(self) -> str:
        """Returns the name of the item."""
        return self.__name

    def get_price(self) -> int:
        """Returns the price of the item."""
        return self.__price

    def get_picture(self) -> tuple[str, ...]:
        """Returns the picture of the item."""
        return self.__picture

    def get_purchase_message(self) -> str:
        return self.__purchase_message

    def __str__(self):
        return str.join('\n', self.__picture)


class Groceries(AbstractItem):
    """
    Groceries. They cost 30.
    """

    def __init__(self):
        purchase_message = '"Hey, that looks pretty tasty!"'
        picture: tuple[str, ...] = tuple(str(x) for x in r"""
  ,--./,-.  
 / #      \ 
|          |
 \        / 
  `._,._,   
        """.split('\n'))  # credit to Hayley Jane Wakenshaw for art
        super().__init__("Groceries", 30, purchase_message, picture)


class HondaCivic(AbstractItem):
    """
    A 2008 Honda Civic. It costs 7072 coins.
    """

    def __init__(self):
        purchase_message = '"Woah dude! That\'s a sick ride. Congrats!"'
        picture: tuple[str, ...] = tuple(str(x) for x in r"""
          _______      
         //  ||\ \     
 \ _____//___||_\ \___ 
   )  _          _    \
 / |_/ \________/ \___|
     \_/        \_/    
        """.split('\n'))  # credit to Colin Douthwaite for art
        super().__init__("2008 Honda Civic", 7072, purchase_message, picture)


class Loan(AbstractItem):
    """
    A special AbstractItem with negative price - but steep interest rates.
    """

    def __init__(self):
        purchase_message = '*Sigh "Just sign there..."'
        picture: tuple[str, ...] = tuple(str(x) for x in r"""
------\ 
| 38% | 
\ APY \ 
 \------
        """.split('\n'))
        super().__init__("Predatory Loan", -2500, purchase_message, picture)


class Rent(AbstractItem):
    """
    Represents paying rent. Yay!
    """

    def __init__(self):
        purchase_message = "You paid rent! 🎉 Your spouse and kid are going to be so proud!"
        picture: tuple[str, ...] = tuple(str(x) for x in r"""
  _______
 |WORLDS |✨
(| BEST  |)
 |RENTER |
  \     /
  `---'
   _|_|_
""".split('\n'))
        super().__init__("Rent", 670, purchase_message, picture)


class PlayerData:
    """
    Represents all long-term player data in CasinoGame, including the number of coins and the items a user has.
    PlayerData is mutable.
    """

    def __init__(self):
        """Constructs PlayerData in the original state where the Player has 1,000 coins and no purchased items."""
        self.__player_coins: int = 1_000
        self.__items: list[AbstractItem] = []

    def get_player_coins(self) -> int:
        """Returns the number of coins the player currently has."""
        return self.__player_coins

    def set_player_coins(self, new_player_coins: int):
        """Sets the number of coins the player currently has."""
        self.__player_coins = new_player_coins

    def add_player_coins(self, coins_to_add: int):
        """Adds coins_to_add coins to the number of coins the player currently has."""
        self.__player_coins += coins_to_add

    def get_items(self) -> tuple[AbstractItem, ...]:
        """Returns a tuple representation of the items the player currently has"""
        return tuple(self.__items)

    def add_item(self, item: AbstractItem):
        """Adds the provided item to the Player's inventory"""
        self.__items.append(item)


class GameState(Enum):
    """
    An enumeration to represent the current state of casino game.

    Attributes:
        MENU: Indicates the game is currently in the main menu.
        MINIGAME: Indicates the game is currently in a minigame.
    """
    MENU = 0
    MINIGAME = 1
    STORE = 2


class MainMenu(AbstractProgram):
    """
    An AbstractProgram used for booting into the other AbstractPrograms of Gambling Simulator.
    """

    def __init__(self, player_data: PlayerData):
        super().__init__()
        self.__player_data = player_data

        # Instantiate graphics
        self.__gambling_simulator_logo = r'''
    $$$$$$\                          $$\       $$\ $$\                           
   $$  __$$\                         $$ |      $$ |\__|                          
   $$ /  \__| $$$$$$\  $$$$$$\$$$$\  $$$$$$$\  $$ |$$\ $$$$$$$\   $$$$$$\        
   $$ |$$$$\  \____$$\ $$  _$$  _$$\ $$  __$$\ $$ |$$ |$$  __$$\ $$  __$$\       
   $$ |\_$$ | $$$$$$$ |$$ / $$ / $$ |$$ |  $$ |$$ |$$ |$$ |  $$ |$$ /  $$ |      
   $$ |  $$ |$$  __$$ |$$ | $$ | $$ |$$ |  $$ |$$ |$$ |$$ |  $$ |$$ |  $$ |      
   \$$$$$$  |\$$$$$$$ |$$ | $$ | $$ |$$$$$$$  |$$ |$$ |$$ |  $$ |\$$$$$$$ |      
    \______/  \_______|\__| \__| \__|\_______/ \__|\__|\__|  \__| \____$$ |      
                                                                 $$\   $$ |      
                                                                 \$$$$$$  |      
 $$$$$$\  $$\                         $$\            $$\          \______/       
$$  __$$\ \__|                        $$ |           $$ |                        
$$ /  \__|$$\ $$$$$$\$$$$\  $$\   $$\ $$ | $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  
\$$$$$$\  $$ |$$  _$$  _$$\ $$ |  $$ |$$ | \____$$\\_$$  _|  $$  __$$\ $$  __$$\ 
 \____$$\ $$ |$$ / $$ / $$ |$$ |  $$ |$$ | $$$$$$$ | $$ |    $$ /  $$ |$$ |  \__|
$$\   $$ |$$ |$$ | $$ | $$ |$$ |  $$ |$$ |$$  __$$ | $$ |$$\ $$ |  $$ |$$ |      
\$$$$$$  |$$ |$$ | $$ | $$ |\$$$$$$  |$$ |\$$$$$$$ | \$$$$  |\$$$$$$  |$$ |      
 \______/ \__|\__| \__| \__| \______/ \__| \_______|  \____/  \______/ \__|      
        '''  # credit https://patorjk.com
        self.__credit_string = "By Daniel Myers, Aiden Kline, Parker Cornelius, and Caleb Arnold"

        # Handling selection
        self.__valid_options = ('blackjack', 'slots', 'roulette', 'store', 'quit')
        self.__selected_option = None

    def _execute(self) -> bool:
        print(self)
        return False

    def _process_input(self, user_input: str) -> bool:
        user_input = user_input.lower()
        if user_input in self.__valid_options:
            self.__selected_option = user_input
            return True
        else:
            print("Enter one of the options above (i.e. blackjack, store, quit): ", end='')
            return False

    def get_selection(self) -> str:
        """Returns the option selected by the user on the MainMenu, none if no option has been selected."""
        return self.__selected_option

    def __str__(self) -> str:
        string_list = []
        # Create a height of 32
        for i in range(29):
            string_list.append('')

        # Create borders
        for i in range(2):
            string_list[i] += '=' * 140
        for i in range(27, 29):
            string_list[i] += '=' * 140

        # Append Gambling Simulator logo in the top left with a width of 80 characters
        gambling_simulator_logo_lines = self.__gambling_simulator_logo.split('\n')
        for row in range(len(gambling_simulator_logo_lines)):
            string_list[row + 2] += f'{gambling_simulator_logo_lines[row]:^80}'

        # Append credit string centered below logo
        string_list[len(gambling_simulator_logo_lines) + 2] += f'{self.__credit_string:^80}'
        string_list[len(gambling_simulator_logo_lines) + 6] += f'{"ENGR 102 Fall 2024":^80}'

        # Append stylized selection options below credits
        selection_display_string = 'Please enter either: '
        for i in range(len(self.__valid_options) - 1):
            selection_display_string += f'{self.__valid_options[i].upper()}, '
        selection_display_string += f'{self.__valid_options[-1].upper()}'

        string_list[len(gambling_simulator_logo_lines) + 3] += f'{'-' * len(selection_display_string):^80}'
        string_list[len(gambling_simulator_logo_lines) + 4] += f'{selection_display_string:^80}'
        string_list[len(gambling_simulator_logo_lines) + 5] += f'{'-' * len(selection_display_string):^80}'

        # Visualize items
        player_items = self.__player_data.get_items()
        player_item_dict: dict[str, AbstractItem] = {item.get_name(): item for item in player_items}

        # Append loan visualization after selection
        if "Predatory Loan" in player_item_dict:
            loan_item = player_item_dict["Predatory Loan"]
            loan_picture = loan_item.get_picture()
            for i in range(len(loan_picture)):
                string_list[len(gambling_simulator_logo_lines) + i + 1] += f'{loan_picture[i]:^10}'
        else:
            for i in range(5):
                string_list[len(gambling_simulator_logo_lines) + i + 1] += ' ' * 10

        # Append car visualization
        if "2008 Honda Civic" in player_item_dict:
            car_item = player_item_dict["2008 Honda Civic"]
            car_picture = car_item.get_picture()
            for i in range(len(car_picture)):
                string_list[len(gambling_simulator_logo_lines) + i - 6] += ' ' * 3 + f'{car_picture[i]:^10}'
        else:
            for i in range(6):
                string_list[len(gambling_simulator_logo_lines) + i - 6] += ' ' * 13

        # Append rent trophy visualization
        if "Rent" in player_item_dict:
            rent_item = player_item_dict["Rent"]
            rent_picture = rent_item.get_picture()
            for i in range(len(rent_picture)):
                string_list[len(gambling_simulator_logo_lines) + i - 15] += ' ' * 3 + f'{rent_picture[i]:^10}'
        else:
            for i in range(7):
                string_list[len(gambling_simulator_logo_lines) + i - 15] += ' ' * 13

        # Append coin visualization after selection
        coin_display_string = f'Coin total: {self.__player_data.get_player_coins():,}'
        if self.__player_data.get_player_coins() <= 0:
            coin_display_string += ' 😭'
        string_list[len(gambling_simulator_logo_lines) + 3] += f'{'-' * len(coin_display_string):^50}'
        string_list[len(gambling_simulator_logo_lines) + 4] += f'{coin_display_string:^50}'
        string_list[len(gambling_simulator_logo_lines) + 5] += f'{'-' * len(coin_display_string):^50}'

        # Return string representation of main menu
        return str.join('\n', string_list)


class GamblingManager:
    """
    This class handles all gambling within CasinoGame. All bets for mini-games are to be made through the
    GamblingManager class to ensure uniformity.
    """

    def __init__(self, player_data: PlayerData):
        """
        Constructs a new GamblingManager with the PlayerData provided. There should only ever be one instance
        of GamblingManager.
        """
        self.__player_data = player_data

    def is_valid_gambling_amount(self, number_of_coins: int) -> bool:
        """
        Returns True if amount is positive and if the player has the amount necessary
        :param number_of_coins: The number of coins to check
        :return: True if amount is positive and if the player has the amount necessary
        """
        return 0 < number_of_coins <= self.__player_data.get_player_coins()

    def place_gamble(self, number_of_coins: int) -> bool:
        """
        Attempts to place the gamble provided, returns False in the event of failure.
        :param number_of_coins: The amount of coins to gamble
        :return: True if the gamble was successfully placed.
        """
        if not self.is_valid_gambling_amount(number_of_coins):
            return False

        self.__player_data.set_player_coins(self.__player_data.get_player_coins() - number_of_coins)
        return True

    def give_player_payout(self, number_of_coins: int) -> None:
        """
        Grants the player the number of coins provided, usually as a reward for victory in gambling.
        :param number_of_coins: The amount of coins to give the player.
        :exception ValueError: If number_of_coins is negative.
        """
        if number_of_coins < 0:
            raise ValueError("Attempted to reward a negative amount of coins.")

        self.__player_data.set_player_coins(self.__player_data.get_player_coins() + number_of_coins)

    def get_player_coins(self) -> int:
        """Returns the number of coins a player has to gamble with."""
        return self.__player_data.get_player_coins()


class Store(AbstractProgram):

    def __init__(self, player_data: PlayerData):
        super().__init__()
        self.__player_data: PlayerData = player_data

        all_items = [Groceries(), HondaCivic(), Rent(), Loan()]

        # Determine unowned items
        player_item_names = [x.get_name() for x in player_data.get_items()]
        self.__store_item_map: dict[str, AbstractItem] = {}
        for item in all_items:
            if item.get_name() not in player_item_names:
                self.__store_item_map[item.get_name().lower()] = item

    def _execute(self) -> bool:
        print("Welcome to the store!")
        self.__prompt_purchase()
        return False

    def _process_input(self, user_input: str) -> bool:
        user_input = user_input.lower()
        if user_input == 'exit':
            print("Thanks for your business!")
            return True

        self.__attempt_purchase(user_input)

        self.__prompt_purchase()
        return False

    def __attempt_purchase(self, item_name: str) -> bool:
        """
        Attempts to purchase an item with the given item name. If successful, the item is added to the
        player's inventory and returns True.
        :param item_name: The name of the item to purchase.
        :return: True if the purchase was successful.
        """
        if not item_name in self.__store_item_map:
            print("Um, I don't think we sell that here...")
            return False
        item = self.__store_item_map[item_name]
        player_coins = self.__player_data.get_player_coins()
        if item.get_price() > player_coins:
            print("Sorry, you don't have enough money!")
            return False
        self.__player_data.set_player_coins(player_coins - item.get_price())
        self.__player_data.add_item(item)
        del self.__store_item_map[item_name]
        print(item.get_purchase_message())
        return True

    def __prompt_purchase(self) -> None:
        print(f"You have {self.__player_data.get_player_coins():,} coins.")
        print("You may purchase any of the following items: ")
        print('-' * 31)
        print(f'|{"Name":<20}|{"Price":<8}|')
        for internal_name, item in self.__store_item_map.items():
            print(f'|{item.get_name():20}|{item.get_price():<8}|')
        print('-' * 31)
        print("What would you like to purchase? (Type exit to leave the store): ")


class GamblingSimulator:
    """
    The primary program of Gambling Simulator.

    The GamblingSimulator class is a representation of the entire Gambling Simulator program.

    Attributes:
        game_state (GameState): The current game state of GamblingSimulator.
        current_abstract_program (Optional[AbstractProgram]): The instance of the AbstractProgram currently being used
            by GamblingSimulator, None if game_state is GameState.MENU
    """

    def __init__(self):
        """Initializes the GamblingSimulator class with 1,000 initial coins"""
        self.player_data: PlayerData = PlayerData()
        self.game_state: GameState = GameState.MENU
        self.current_abstract_program: Optional[AbstractProgram] = MainMenu(self.player_data)

        self.__gambling_manager = GamblingManager(self.player_data)

    def execute_program(self) -> None:
        """Starts the primary gameplay loop of GamblingSimulator."""
        # todo insert startup logic here
        complete = self.current_abstract_program.execute_program()
        if not complete:
            self.run_game()

    def run_game(self) -> None:
        """The gameplay loop of GamblingSimulator."""
        playing = True
        while playing:
            user_input = input()
            playing = not self.process_user_input(user_input)

    def process_user_input(self, user_input: str) -> bool:
        match self.game_state:
            case GameState.MENU:
                selection_made = self.current_abstract_program.process_user_input(user_input)
                if selection_made:
                    selection = cast(MainMenu, self.current_abstract_program).get_selection()
                    match selection:
                        case 'blackjack':
                            self.game_state = GameState.MINIGAME
                            self.current_abstract_program = BlackjackMinigame(self.__gambling_manager)
                        case 'slots':
                            self.game_state = GameState.MINIGAME
                            self.current_abstract_program = SlotsMinigame(self.__gambling_manager)
                        case 'roulette':
                            self.game_state = GameState.MINIGAME
                            self.current_abstract_program = RouletteMinigame(self.__gambling_manager)
                        case 'store':
                            self.game_state = GameState.STORE
                            self.current_abstract_program = Store(self.player_data)
                        case 'credits':
                            pass # may implement credits in the future
                        case 'quit':
                            print("Thanks for playing!")
                            return True
                    self.current_abstract_program.execute_program()
            case GameState.MINIGAME:
                minigame_complete = self.current_abstract_program.process_user_input(user_input)
                if minigame_complete:
                    self.game_state = GameState.MENU
                    self.current_abstract_program = MainMenu(self.player_data)
                    self.current_abstract_program.execute_program()
            case GameState.STORE:
                store_complete = self.current_abstract_program.process_user_input(user_input)
                if store_complete:
                    self.game_state = GameState.MENU
                    self.current_abstract_program = MainMenu(self.player_data)
                    self.current_abstract_program.execute_program()
        return False


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

        self.__money_pool = None

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
            self.__money_pool = attempted_bet
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
                winnings = 2 * round(self.__money_pool - (self.__money_pool * (payout_odds)))
                print(f"Congratulations! You won {winnings} coins on number {result}.")
            else:
                print(f"L, {result}")

        # Color betting results
        elif self.__bet_type == 'color':
            if bet_color == result_color:
                if bet_color == 'red' or bet_color == 'black':
                    winnings = 2 * self.__money_pool
                    print(f"Congratulations! You won {winnings} coins on {result_color}.")
                elif bet_color == 'green':
                    winnings = round(self.__money_pool * 36)
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


class ExecutionNotInitiatedException(Exception):
    """A continuation method of AbstractMethod was called without first initiating execution."""

    def __init__(self, *args):
        super().__init__(*args)


class AlreadyExecutedException(Exception):
    """An AbstractProgram was attempted to be executed using execute_program(self) when it was already executed."""

    def __init__(self, *args):
        super().__init__(*args)


class AbstractProgramCompleteException(Exception):
    """An AbstractProgram was attempted to be executed when it already completed execution."""

    def __init__(self, *args):
        super().__init__(*args)

game = GamblingSimulator()
game.execute_program()
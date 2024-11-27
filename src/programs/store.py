from src.items.abstract_item import AbstractItem
from src.items.groceries import Groceries
from src.items.honda_civic import HondaCivic
from src.items.loan import Loan
from src.items.rent import Rent
from src.player_data import PlayerData
from src.programs.abstract_program import AbstractProgram


class Store(AbstractProgram):

    def __init__(self, player_data: PlayerData):
        super().__init__()
        self.__player_data: PlayerData = player_data

        all_items = [Groceries(), HondaCivic(), Rent(), Loan()]  # todo add more items

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

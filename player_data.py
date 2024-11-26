from items.abstract_item import AbstractItem


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

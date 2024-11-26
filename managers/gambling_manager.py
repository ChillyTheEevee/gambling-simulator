from player_data import PlayerData


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

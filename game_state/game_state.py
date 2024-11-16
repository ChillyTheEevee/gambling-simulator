from enum import Enum

class GameState(Enum):
    """
    An enumeration to represent the current state of casino game.

    Attributes:
        MENU: Indicates the game is currently in the main menu.
        MINIGAME: Indicates the game is currently in a minigame.
    """
    MENU = 0
    MINIGAME = 1
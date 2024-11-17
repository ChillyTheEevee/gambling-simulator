from typing import Optional

from game_state.game_state import GameState
from programs.abstract_program import AbstractProgram


class CasinoGame:
    """
    The primary program of Casino Game.

    The CasinoGame class is a representation of the entire Casino Game program.

    Attributes:
        coins (int): How many coins the user has
        items (list): A list of items that the user has bought
        game_state (GameState): The current game state of CasioGame
        current_abstract_program (Optional[AbstractProgram]): The instance of the AbstractProgram currently being used
            by CasinoGame, None if game_state is GameState.MENU
    """

    def __init__(self):
        """Initializes the CasinoGame class with 1,000 initial coins"""
        self.coins: int = 1_000
        self.items: list = []
        self.game_state: GameState = GameState.MENU
        self.current_abstract_program: Optional[AbstractProgram] = None

    def execute_program(self) -> None:
        """Starts the primary gameplay loop of this CasinoGame."""
        # todo insert startup logic here
        self.run_game()

    def run_game(self) -> None:
        """The gameplay loop of this CasinoGame."""
        playing = True
        while playing:
            user_input = input()
            playing = not self.process_user_input(user_input)

    def process_user_input(self, user_input: str) -> bool:
        match self.game_state:
            case GameState.MENU:
                pass  # todo implement menu, minigame selection and booting
            case GameState.MINIGAME:
                self.current_abstract_program.process_user_input(user_input)
        return False
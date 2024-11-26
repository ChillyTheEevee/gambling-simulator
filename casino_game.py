from typing import Optional

from game_state.game_state import GameState
from player_data import PlayerData
from programs.abstract_program import AbstractProgram


class CasinoGame:
    """
    The primary program of Casino Game.

    The CasinoGame class is a representation of the entire Casino Game program.

    Attributes:
        game_state (GameState): The current game state of CasioGame
        current_abstract_program (Optional[AbstractProgram]): The instance of the AbstractProgram currently being used
            by CasinoGame, None if game_state is GameState.MENU
    """

    def __init__(self):
        """Initializes the CasinoGame class with 1,000 initial coins"""
        self.player_data: PlayerData = PlayerData()
        self.game_state: GameState = GameState.MENU
        self.current_abstract_program: Optional[AbstractProgram] = None

        self.__gamble_manager = GambleManager(self.player_data)

    def execute_program(self) -> None:
        """Starts the primary gameplay loop of this CasinoGame."""
        # todo insert startup logic here
        print("Starting CasinoGame...")
        complete = self.current_abstract_program.execute_program()
        if not complete:
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
                minigame_complete = self.current_abstract_program.process_user_input(user_input)
                if minigame_complete:
                    self.game_state = GameState.MENU
                    self.current_abstract_program = None
        return False
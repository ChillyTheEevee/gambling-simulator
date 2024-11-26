from typing import Optional
from typing import cast

from game_state.game_state import GameState
from managers.gambling_manager import GamblingManager
from player_data import PlayerData
from programs.abstract_program import AbstractProgram
from programs.main_menu import MainMenu
from programs.minigames.blackjack import BlackjackMinigame
from programs.minigames.roulette import RouletteMinigame
from programs.minigames.slots import SlotsMinigame


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
        self.current_abstract_program: Optional[AbstractProgram] = MainMenu()

        self.__gambling_manager = GamblingManager(self.player_data)

    def execute_program(self) -> None:
        """Starts the primary gameplay loop of this CasinoGame."""
        # todo insert startup logic here
        print("Starting CasinoGame...")
        complete = self.current_abstract_program.execute_program()
        if not complete:
            self.run_game()

    def run_game(self) -> None:
        """The gameplay loop of CasinoGame."""
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
                    self.current_abstract_program.execute_program()
            case GameState.MINIGAME:
                minigame_complete = self.current_abstract_program.process_user_input(user_input)
                if minigame_complete:
                    self.game_state = GameState.MENU
                    self.current_abstract_program = MainMenu()
                    self.current_abstract_program.execute_program()
        return False

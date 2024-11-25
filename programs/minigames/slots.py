from typing import override

from player_data import PlayerData
from programs.abstract_program import AbstractProgram


class SlotsMinigame(AbstractProgram):
    """
    A simple slot machine minigame.

    Written by Caleb Arnold. Adapted to the AbstractProgram interface by Daniel Myers.
    """

    def __init__(self, player_data: PlayerData):
        super().__init__()
        self.__player_data = player_data

    @override
    def _execute(self) -> bool:
        pass

    @override
    def _process_input(self, user_input: str) -> bool:
        pass
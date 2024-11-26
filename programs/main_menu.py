from programs.abstract_program import AbstractProgram


class MainMenu(AbstractProgram):

    def __init__(self):
        super().__init__()
        self.__valid_options = ('blackjack', 'slots', 'roulette')
        self.__selected_option = None

    def _execute(self) -> bool:
        print("Welcome to Gambling Simulator!")
        print("Which game would you like to play?")
        print("(blackjack, slots, roulette): ", end='')
        return False

    def _process_input(self, user_input: str) -> bool:
        if user_input in self.__valid_options:
            self.__selected_option = user_input
            return True
        else:
            print("Please enter either blackjack, slots, or roulette: ", end='')
            return False

    def get_selection(self):
        return self.__selected_option
from player_data import PlayerData
from programs.abstract_program import AbstractProgram


class MainMenu(AbstractProgram):

    def __init__(self, player_data: PlayerData):
        super().__init__()
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
        ''' # todo credit https://patorjk.com
        self.__credit_string = "By Daniel Myers, Aiden Kline, Parker Cornelius, and Caleb Arnold"

        # Handling selection
        self.__valid_options = ('blackjack', 'slots', 'roulette', 'quit')
        self.__selected_option = None

    def _execute(self) -> bool:
        print(self)
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
            string_list[row+2] += f'{gambling_simulator_logo_lines[row]:^80}'

        # Append credit string centered below logo
        string_list[len(gambling_simulator_logo_lines) + 2] += f'{self.__credit_string:^80}'
        # Return string representation of main menu
        return str.join('\n', string_list)
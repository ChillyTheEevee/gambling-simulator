from src.items.abstract_item import AbstractItem
from src.player_data import PlayerData
from src.programs.abstract_program import AbstractProgram


class MainMenu(AbstractProgram):
    """
    An AbstractProgram used for booting into the other AbstractPrograms of Gambling Simulator.
    """
    def __init__(self, player_data: PlayerData):
        super().__init__()
        self.__player_data = player_data

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
 \______/ \__|\__| \__| \__| \______/ \__| \_______|  \____/  \______/ \__|      ''' # todo credit https://patorjk.com
        self.__credit_string = "By Daniel Myers, Aiden Kline, Parker Cornelius, and Caleb Arnold"
        self.__version_string = "ENGR 102 Fall 2024 v1.0"

        # Handling selection
        self.__valid_options = ('blackjack', 'slots', 'roulette', 'store', 'quit')
        self.__selected_option = None

    def _execute(self) -> bool:
        print(self)
        return False

    def _process_input(self, user_input: str) -> bool:
        user_input = user_input.lower()
        if user_input in self.__valid_options:
            self.__selected_option = user_input
            return True
        else:
            print("Enter one of the options above (i.e. blackjack, store, quit): ", end='')
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
        string_list[len(gambling_simulator_logo_lines) + 6] += f'{self.__version_string:^80}'

        # Append stylized selection options below credits
        selection_display_string = 'Please enter either: '
        for i in range(len(self.__valid_options)-1):
            selection_display_string += f'{self.__valid_options[i].upper()}, '
        selection_display_string += f'{self.__valid_options[-1].upper()}'

        string_list[len(gambling_simulator_logo_lines) + 3] += f'{'-' * len(selection_display_string):^80}'
        string_list[len(gambling_simulator_logo_lines) + 4] += f'{selection_display_string:^80}'
        string_list[len(gambling_simulator_logo_lines) + 5] += f'{'-' * len(selection_display_string):^80}'

        # Visualize items
        player_items = self.__player_data.get_items()
        player_item_dict: dict[str, AbstractItem] = {item.get_name(): item for item in player_items}

        # Append loan visualization after selection
        if "Predatory Loan" in player_item_dict:
            loan_item = player_item_dict["Predatory Loan"]
            loan_picture = loan_item.get_picture()
            for i in range(len(loan_picture)):
                string_list[len(gambling_simulator_logo_lines) + i + 1] += f'{loan_picture[i]:^10}'
        else:
            for i in range(5):
                string_list[len(gambling_simulator_logo_lines) + i + 1] += ' ' * 10

        # Append car visualization
        if "2008 Honda Civic" in player_item_dict:
            car_item = player_item_dict["2008 Honda Civic"]
            car_picture = car_item.get_picture()
            for i in range(len(car_picture)):
                string_list[len(gambling_simulator_logo_lines) + i -6] += ' ' * 3 + f'{car_picture[i]:^10}'
        else:
            for i in range(6):
                string_list[len(gambling_simulator_logo_lines) + i -6] += ' ' * 13

        # Append rent trophy visualization
        if "Rent" in player_item_dict:
            rent_item = player_item_dict["Rent"]
            rent_picture = rent_item.get_picture()
            for i in range(len(rent_picture)):
                string_list[len(gambling_simulator_logo_lines) + i -15] += ' ' * 3 + f'{rent_picture[i]:^10}'
        else:
            for i in range(7):
                string_list[len(gambling_simulator_logo_lines) + i -15] += ' ' * 13

        # Append coin visualization after selection
        coin_display_string = f'Coin total: {self.__player_data.get_player_coins():,}'
        if self.__player_data.get_player_coins() <= 0:
            coin_display_string += ' 😭'
        string_list[len(gambling_simulator_logo_lines) + 3] += f'{'-' * len(coin_display_string):^50}'
        string_list[len(gambling_simulator_logo_lines) + 4] += f'{coin_display_string:^50}'
        string_list[len(gambling_simulator_logo_lines) + 5] += f'{'-' * len(coin_display_string):^50}'

        # Return string representation of main menu
        return str.join('\n', string_list)
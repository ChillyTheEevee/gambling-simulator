from src.items.abstract_item import AbstractItem


class HondaCivic(AbstractItem):
    """
    A 2008 Honda Civic. It costs 7072 coins.
    """

    def __init__(self):
        purchase_message = '"Woah dude! That\'s a sick ride. Congrats!"'
        picture: tuple[str, ...] = tuple(str(x) for x in r"""
          _______      
         //  ||\ \     
 \ _____//___||_\ \___ 
   )  _          _    \
 / |_/ \________/ \___|
     \_/        \_/    
        """.split('\n')) # credit to Colin Douthwaite for art
        super().__init__("2008 Honda Civic", 7072, purchase_message, picture)
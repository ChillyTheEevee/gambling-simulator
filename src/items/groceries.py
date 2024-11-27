from src.items.abstract_item import AbstractItem


class Groceries(AbstractItem):
    """
    Groceries. They cost 30.
    """

    def __init__(self):
        purchase_message = '"Hey, that looks pretty tasty!"'
        picture: tuple[str, ...] = tuple(str(x) for x in r"""
  ,--./,-.  
 / #      \ 
|          |
 \        / 
  `._,._,   
        """.split('\n')) # credit to Hayley Jane Wakenshaw for art
        super().__init__("Groceries", 30, purchase_message, picture)
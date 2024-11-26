from abc import ABC

from items.abstract_item import AbstractItem


class Groceries(AbstractItem):
    """
    Groceries. They cost 30.
    """

    def __init__(self):
        purchase_message = "Just sign there, there, and there."
        picture: tuple[str] = tuple(str(r"""
  ,--./,-.
 / #      \
|          |
 \        /
  `._,._,
        """.split('\n'))) # todo credit Hayley Jane Wakenshaw for art
        super().__init__("Groceries", 30, purchase_message, picture)
from abc import ABC

from items.abstract_item import AbstractItem


class Rent(AbstractItem):
    """
    Represents paying rent. Yay!
    """

    def __init__(self):
        purchase_message = "You paid rent! 🎉 Your spouse and kid are going to be so proud!"
        picture: tuple[str, ...] = tuple(str(x) for x in r"""
  _______
 |WORLDS |✨
(| BEST  |)
 |RENTER |
  \     /
  `---'
   _|_|_
""".split('\n'))
        super().__init__("Rent", 670, purchase_message, picture)
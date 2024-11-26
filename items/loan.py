from abc import ABC

from items.abstract_item import AbstractItem


class Loan(AbstractItem):
    """
    A special AbstractItem with negative price - but steep interest rates.
    """

    def __init__(self):
        purchase_message = '*Sigh "Just sign there..."'
        picture: tuple[str] = tuple(str(r"""
------\ 
| 38% | 
\ APY \ 
 \------
        """.split('\n')))
        super().__init__("Predatory Loan", -2500, purchase_message, picture)
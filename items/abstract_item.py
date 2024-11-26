from abc import ABC


class AbstractItem(ABC):
    """
    An AbstractItem is an Item that a name, price, purchase message, and a picture that can be displayed.

    The __str__ method of an AbstractItem returns the picture of the Item in string form.
    """

    def __init__(self, name: str, price: int, purchase_message: str, picture: tuple[str]):
        self.__name: str = name
        self.__price: int = price
        self.__picture: tuple[str] = picture
        self.__purchase_message:str = purchase_message

    def get_name(self) -> str:
        """Returns the name of the item."""
        return self.__name

    def get_price(self) -> int:
        """Returns the price of the item."""
        return self.__price

    def get_picture(self) -> tuple[str]:
        """Returns the picture of the item."""
        return self.__picture

    def get_purchase_message(self) -> str:
        return self.__purchase_message

    def __str__(self):
        return str.join('\n', self.__picture)

"""
Player is the virtual player instance in the game
Contains inventory, and maybe some other attributes

TODO: Allow devs to subclass Player to add custom functionality
"""


class Player:
    def __init__(self):
        # TODO: Make inventory a list with name to item dict like in room.py
        self.inventory = {}

    class ItemNotInInventoryError(KeyError):
        pass

    def get_item(self, nouns, default=None):
        """
        Returns a reference to the item in inventory with name=noun
        """
        if not nouns:
            return default

        for noun in nouns:
            try:
                return self.inventory[noun]
            except KeyError:
                continue
        else:
            return default
            # raise self.ItemNotInInventoryError(f"{nouns[0]} not in inventory")

    def pop_item(self, noun):
        """
        Returns a reference to the item in inventory with name=noun,
        and deletes all references to it in the inventory dict
        """
        item = self.get_item(noun)

        for name in item.names:
            del self.inventory[name]

        return item

    def __iter__(self):
        """
        Returns an iterator to the items in the Player's inventory
        """
        return iter(self.inventory.values())

    def __str__(self):
        return f"{self.__class__.__name__}"

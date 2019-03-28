from lester.synonym import SynonymFinder


class RoomMeta(type):
    def __new__(mcs, name, bases, attrs):
        from lester.item import Item

        attrs['items'] = [
            item()
            for item in attrs.values()
            if hasattr(item, '__bases__')
            if Item in item.__bases__
        ]

        if not bases:  # To create a Room superclass with this Metaclass
            return super().__new__(mcs, name, bases, attrs)

        if 'names' not in attrs:
            if 'name' in attrs:
                # Allow users to specify only one name
                attrs['names'] = [attrs['name']]
            else:
                raise AttributeError(f"names attribute is required on {name}")
        if 'description' not in attrs:
            raise AttributeError(f"description attribute is required on {name}")

        attrs['names'] = [name.lower() for name in attrs['names']]

        return super().__new__(mcs, name, bases, attrs)


class Room(metaclass=RoomMeta):
    names = []
    description = ""
    items = []
    noun_to_item = {}

    connected_rooms = []

    class ItemNotInRoomError(KeyError):
        pass

    def __new__(cls, *args, **kwargs):
        cls.__map_name_to_item()
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def __map_name_to_item(cls):
        cls.noun_to_item = {
            synonym: item
            for item in cls.items
            for synonym in SynonymFinder(*item.names).get()
        }

    @property
    def name(self):
        return self.names[0]

    def get_item(self, noun, default=None):
        try:
            return self.noun_to_item[noun]
        except KeyError:
            return default

    def pop_item(self, noun):
        """
        Returns a reference to the item in the room with name=noun, deletes refs
        in the rooms item dictionary
        TODO: Research lazy deletion instead
        """
        item = self.get_item(noun)

        if item is None:
            raise self.ItemNotInRoomError

        for noun, item in self.noun_to_item.items():
            del self.noun_to_item[noun]

        return item

    def display(self, short=False):
        """
        Prints a description of the current room
        # TODO: Figure out a way to see adjoining rooms, no dunder item!
        """
        print(f"{self.names[0].title()}")
        print(f"{self.description}")

        if not short:
            for item in self:
                print(f"{item.short_description}")

    def on_enter(self):
        """
        Automatically prints look short text
        """
        self.display(short=True)

    def on_exit(self):
        pass

    def __iter__(self):
        """
        Returns an iterator for the items in the Room
        """
        return iter(self.items)

    def __str__(self):
        return f"{self.__class__.__name__} <{self.names[0]} - {self.description}>"

from lester import constants

from lester.action import Action

from lester.synonym import SynonymFinder


class ItemMeta(type):
    def __new__(mcs, name, bases, attrs):
        attrs['actions'] = [
            action()
            for action in attrs.values()
            if hasattr(action, '__bases__')
            if Action in action.__bases__
        ]

        if not bases:  # To create an Item superclass with this Metaclass
            return super().__new__(mcs, name, bases, attrs)

        for base in bases:
            # Allow Action inheritance on subclassing of Item
            attrs['actions'].extend(base.actions)

        if 'names' not in attrs:
            if 'name' in attrs:
                # Allow users to specify only one name
                attrs['names'] = [attrs['name']]
            else:
                raise AttributeError(f"names attribute is required on {name}")
        if 'description' not in attrs:
            raise AttributeError(f"description attribute is required on {name}")
        if 'short_description' not in attrs:
            raise AttributeError(
                f"short_description attribute is required on {name}"
            )

        attrs['names'] = [name.lower() for name in attrs['names']]
        attrs['obtainable'] = attrs.pop('obtainable', False)

        return super().__new__(mcs, name, bases, attrs)


class Item(metaclass=ItemMeta):
    names = []
    description = ""
    short_description = ""
    obtainable = False
    actions = []
    verb_to_action = {}

    class BadVerbError(KeyError):
        pass

    def __new__(cls, *args, **kwargs):
        cls.__map_verb_to_action()
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def __map_verb_to_action(cls):
        cls.verb_to_action = {
            synonym: action
            for action in cls.actions
            for synonym in SynonymFinder(*action.verbs,
                                         part_of_speech=SynonymFinder.VERB).get()
        }

    @property
    def name(self):
        return self.names[0]

    class Look(Action):
        """
        All Items have this Action by default, which prints its description
        """
        name = 'look'
        verbs = constants.LOOK_VERBS

        def do(self, context):
            print(f"{context.item.description}")

    def get_action(self, verb, default=None):
        """
        Returns a reference to the action for this Item with Verb=verb
        """
        if not verb:
            return default

        try:
            return self.verb_to_action[verb]
        except KeyError:
            return default

    def __iter__(self):
        """
        Returns an iterator the Actions applicable to the Item
        """
        return iter(self.actions)

    def __str__(self):
        return f"{self.__class__.__name__} " \
            f"<{self.names[0]} - {self.short_description}>"

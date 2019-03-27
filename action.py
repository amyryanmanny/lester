class ActionMeta(type):
    """
    This doesn't really do anything, but maybe someday
    """
    def __new__(mcs, name, bases, attrs):
        if not bases:  # To create an Action superclass with this Metaclass
            return super().__new__(mcs, name, bases, attrs)

        return super().__new__(mcs, name, bases, attrs)


class Action(metaclass=ActionMeta):
    verbs = []

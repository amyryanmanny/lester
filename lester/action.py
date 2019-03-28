if False:
    # TODO: There has to be a better way to do this
    from lester.context import Context


class ActionMeta(type):
    def __new__(mcs, name, bases, attrs):
        if not bases:  # To create an Action superclass with this Metaclass
            return super().__new__(mcs, name, bases, attrs)

        if 'verbs' not in attrs:
            raise AttributeError(f"{name} must have a list of verbs")
        if not getattr(attrs['verbs'], '__iter__', None):
            raise AttributeError(f"{name}'s verbs must be iterable")

        if 'do' not in attrs:
            raise AttributeError(f"{name} must have a do method defined")
        elif not callable(attrs['do']):
            raise AttributeError(f"{name}'s do method is not callable")

        # Astonishes user by not forcing them to pass in self
        # TODO: Figure out if it can just replace self with context instead
        attrs['do'] = staticmethod(attrs['do'])

        return super().__new__(mcs, name, bases, attrs)


class Action(metaclass=ActionMeta):
    verbs = []

    @staticmethod
    def do(context: 'Context'):
        """
        This base function exists to improve linting
        """
        raise NotImplementedError

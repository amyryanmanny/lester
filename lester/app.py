"""
The App is the parent to all Rooms, Items, and the Player
It handles all text parsing and action handling

TODO: Replace input/print statements with pipes to decouple interface
"""

from lester.context import Context
from lester.player import Player

from lester.parser import Parser

from lester import constants


class App:
    __apps = {}

    class RoomDoesNotExist(ValueError):
        pass

    def __init__(self, name):
        self.__player = Player()
        self.__name = name
        self.__rooms = {}

        # Parser generated on start(), since it needs references to the objects
        self.__parser = None

        self.current_room = None

    def register(self, cls):
        """
        Decorator (or function) that registers a Room class with the app
        """
        from lester.room import Room

        if not issubclass(cls, Room):
            # This might change eventually
            raise ValueError("Only Room classes can be registered with App")

        room = cls()
        for room_name in cls.names:
            self.__rooms[room_name] = room

        return cls  # Return the class itself to reduce astonishment

    @classmethod
    def get_app(cls, app_name='app'):
        """
        Apps are stored as name-based Singletons because that seemed like the
        best way to do it for some reason
        """
        if app_name not in cls.__apps:
            app = cls(app_name)
            cls.__apps[app_name] = app
        return cls.__apps[app_name]

    @property
    def player(self):
        """
        It should not be possible to set the Player
        Instead, use the provided interfaces on the Player to reset her
        """
        return self.__player

    def change_room(self, room_name):
        """
        Changes room and executes appropriate Room.on_enter/exit methods
        Set self.room directly to avoid that behavior in rare cases
        Implements the State Pattern
        """
        try:
            room = self.__rooms[room_name.lower()]
        except KeyError:
            raise self.RoomDoesNotExist(f"{room_name.title()} does not exist in {self}")

        if self.current_room is not None:
            self.current_room.on_exit()
        self.current_room = room
        self.current_room.on_enter()

    def parse(self, s):
        """
        Passes string into the Parser
        """
        return self.__parser.parse(s)

    def run_loop(self):
        """
        This is where the game actually takes place
        Handles all logic
        """
        while True:
            s = input("> ").lower()
            try:
                verb, nouns = self.parse(s)
            except Parser.NoVerbsError:
                print("I don't know how to do that")
                continue
            except Parser.TooManyVerbsError:
                print("I can't do that many things at once")
                continue
            except Exception:
                # TODO: Log these lines
                print(f"REALLY INVALID COMMAND: {s}")
                continue

            if verb in constants.LOOK_VERBS:
                if not nouns:
                    self.current_room.display()
                    continue

            if verb in constants.GO_VERBS:
                if nouns:
                    room = nouns[-1]
                    if room in self.current_room.connected_rooms:
                        self.change_room(room)
                    else:
                        print(f"I don't know how to get to {room}")
                    continue
                else:
                    print("Where should I go?")
                    continue

            if nouns:
                subject = self.current_room.get_item(nouns)
                _object = self.player.get_item(nouns)
            else:
                # All verb-only commands should already be handled
                print(f"What should I {verb}?")
                continue

            if subject is not None:
                assert subject is not _object  # Bug alert! Bail me out

            action = None
            if subject is not None:
                # Try the verb with the subject first
                action = subject.get_action(verb)
            if action is None and _object is not None:
                action = _object.get_action(verb)
            if action is None:
                print(f"I don't know how to {verb} {nouns[-1]}")
                continue

            action.do(
                context=Context(
                    player=self.player,
                    room=self.current_room,
                    item=subject,
                    tool=_object,
                )
            )

    def start(self, starting_room_name):
        self.__parser = Parser(self.__rooms.values())

        if isinstance(starting_room_name, str):
            self.change_room(starting_room_name)
        else:
            raise NotImplementedError

        self.run_loop()

    def __iter__(self):
        # This might be junk
        return iter(self.__rooms.values())

    def __str__(self):
        return f"{self.__class__.__name__} <{self.__name}>"

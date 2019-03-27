"""
Context objects hold the surrounding context that an Action is taking place in
"""


class Context:
    def __init__(self, player, room, item, tool):
        self.player = player
        self.room = room
        self.item = item
        self.tool = tool

    def __str__(self):
        return "Context:\n" + "\n\t".join(
            [str(o) for o in [self.player, self.room, self.item, self.tool]]
        )

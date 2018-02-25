from jc2cli.command import Command
from jc2cli.mode import Mode


class Node(object):
    """Node class implements all functionality for storing command information
    in the command tree.

    The command tree is composed by modes, which contain commands or modes.
    """

    def __init__(self, name, cb=None, mode=False):
        self.name = name
        self.__original_name = name
        if cb and not mode:
            self.command = Command(cb)
        elif cb and mode:
            self.command = Mode(cb)
        else:
            self.command = None
        self.loaded = True
        self.enabled = True

    def is_command(self):
        return not isinstance(self.command, Mode)

    def is_mode(self):
        return isinstance(self.command, Mode)

    def is_usable(self):
        """is_usable returns if the command is loaded and enabled.
        """
        return self.enabled and self.loaded

from jc2cli.command import Command
from jc2cli.mode import Mode


class Node(object):

    def __init__(self, name, cb=None, mode=False):
        self.name = name
        self.__original_name = name
        if cb and not mode:
            self.command = Command(cb)
        elif cb and mode:
            self.command = Mode(cb)
        else:
            self.command = None

    def is_command(self):
        return not isinstance(self.command, Mode)

    def is_mode(self):
        return isinstance(self.command, Mode)

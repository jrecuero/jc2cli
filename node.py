from command import Command


class Node(object):

    def __init__(self, name, cb=None):
        self.name = name
        self.__original_name = name
        self.command = Command(cb) if cb else None

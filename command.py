class Command(object):

    def __init__(self, cb):
        self.cb = cb
        self._syntax = None
        self.name = None
        self.params = {}

    @property
    def syntax(self):
        return self._syntax

    @syntax.setter
    def syntax(self, value):
        self._syntax = value
        self.name = self.syntax.split()[0]

    def add_param(self, key, value):
        self.params[key] = value

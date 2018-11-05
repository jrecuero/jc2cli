from jc2cli.syntax.content import Content
from jc2cli.syntax.completer import CompleterArgument


class Argument(Content):

    def __init__(self, label, _help, _type, completer=None):
        super(Argument, self).__init__(label, _help, completer)
        self._type = _type
        self._default = None

    def setup(self):
        if self.completer is None:
            self.completer = CompleterArgument(self.label)
        return self

    def get_type(self):
        return self._type

    def cast(self, value):
        return str(value)

    def assign(self, value):
        return str(value)

    def is_argument(self):
        return True

    def get_str_type(self):
        return 'A'


class ArgumentString(Argument):

    def __init__(self, label, _help, completer=None):
        super(Argument, self).__init__(label, _help, 'str', completer)

    def get_str_type(self):
        return 'S'


class ArgumentInt(Argument):

    def __init__(self, label, _help, completer=None):
        super(Argument, self).__init__(label, _help, 'int', completer)

    def cast(self, value):
        return int(value)

    def assign(self, value):
        return int(value)

    def get_str_type(self):
        return 'I'

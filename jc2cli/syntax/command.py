from jc2cli.syntax.content import Content
from jc2cli.syntax.command_syntax import CommandSyntax
from jc2cli.syntax.completer import CompleterCommand


class Command(Content):

    def __init__(self, parent, label, _help, completer=None):
        super(Command, self).__init__(label, _help, completer)
        self.syntax_str = None
        self.syntax = None
        self.arguments = []
        self.parent = None
        self.has_children = False
        self.is_builtin = False
        self.run_as_no_final = False
        self.just_prefix = False
        self.prompt = None
        self.is_mode = False

    def get_str_type(self):
        return 'M' if self.is_mode else 'C'

    def look_for_argument(self, label):
        for argo in self.arguments:
            if argo.label = label:
                return argo
        return None

    def setup(self):
        self.syntax = CommandSyntax(self.syntax_str)
        if self.completer is None:
            self.completer = CompleterCommand(self.label)
        for argo in self.arguments:
            argo.setup()
        return self

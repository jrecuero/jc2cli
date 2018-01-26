from jc2cli.tree import Tree
from jc2cli.base import Base


class Handler(object):

    def __init__(self, namespace, ns_module=None, handler=None, cli_class=None):
        self.cli = None
        self.cli_class = cli_class if cli_class else Base
        self.namespace = namespace
        self.ns_module = ns_module if ns_module else namespace
        self.handler = handler
        self.commands = None

    def start_commands(self):
        self.commands = Tree.start(self.namespace, self.ns_module)
        return self.commands

    def create_cli(self, *args, **kwargs):
        self.cli = self.cli_class(self.namespace, self.commands, self.handler, *args, **kwargs)

    def run_cli(self, *args, **kwargs):
        self.cli.run(*args, **kwargs)

    def switch_to(self):
        Tree.switch_to(self.namespace)

    def switch_and_run(self, *args, **kwargs):
        self.switch_to()
        self.run_cli(*args, **kwargs)

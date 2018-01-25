from jc2cli.tree import Tree
from jc2cli.base import Base


class Handler(object):

    def __init__(self, namespace, ns_module=None, handler=None):
        self.cli = None
        self.namespace = namespace
        self.ns_module = ns_module if ns_module else namespace
        self.handler = handler

    def start_commands(self):
        self.commands = Tree.start(self.namespace, self.ns_module)
        return self.commands

    def create_cli(self):
        self.cli = Base(self.namespace, self.commands, self.handler)

    def run_cli(self):
        self.cli.run()

    def switch_to(self):
        Tree.switch_to(self.namespace)

    def switch_and_run(self):
        self.switch_to()
        self.run_cli()

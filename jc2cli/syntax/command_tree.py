from jc2cli.graph.graph import Graph
from jc2cli.syntax.content_node import ContentNode


class CommandTree(Graph):

    def __init__(self):
        super(CommandTree, self).__init__()

    def add_to(self, parent, command):
        if parent is None:
            parent = self.root
            node = ContentNode(command.label, command)
            parent.add_child(node)
            return node

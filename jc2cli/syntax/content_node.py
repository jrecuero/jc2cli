from jc2cli.graph.node import Node


class ContentNode(Node):

    def __init__(self, label, content):
        super(ContentNode, self).__init__(label, content)

    def match(self, context, tokens, index):
        if self.content.completer is not None:
            return self.content.completer.match(context, self.content, tokens, index)
        if tokens[index] == self.content.label:
            return index + 1, True
        return index, False

    def query(self, context, tokens, index):
        if self.content.completer is not None:
            return self.content.completer.query(context, self.content, tokens, index)
        return None, True

    def help(self, context, tokens, index):
        if self.content.completer is not None:
            result = []
            if self.is_content or self.is_sink:
                return self.content.completer.help(context, self.content, tokens, 0)
            else:
                for child_node in self.children:
                    result.append(child_node.help(context, tokens, 0))
                return result, True
        return self.conent.label, True

from jc2cli.syntax.joint import get_cr


class Matcher:

    def __init__(self, ctx, grapher):
        self.context = ctx
        self.grapher = grapher
        self.rooter = None

    def _match_command_line(self, tokens):
        tokens.append(get_cr())
        index, ok = self._match_with_graph(tokens)
        if not ok or index != len(tokens):
            return False
        return True

    def _traverse_and_match_graph(self, node, tokens, index):
        if index >= len(tokens):
            return None, index, False
        for child_node in node.children:
            index_matched, ok = child_node.match(self.context, tokens, index)
            if not ok:
                return None, index, False
            _child_node = child_node
            while index_matched == index:
                _child_node, index_matched, ok = self.traverse_and_match_graph(_child_node, tokens, index_matched)
                if not ok:
                    break
            if index_matched != index:
                return _child_node, index_matched, True
        return None, index, False

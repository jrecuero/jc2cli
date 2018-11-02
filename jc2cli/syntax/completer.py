from jc2cli.syntax.tokens import Token


class Completer:

    def __init__(self, label):
        self.label = label

    def validate(context, content, tokens, index):
        return True

    def help(context, content, tokens, index):
        return None, False

    def query(context, content, tokens, index):
        return None, False

    def complete(context, content, tokens, index):
        return None, False

    def match(context, content, tokens, index):
        return -1, False

    def _complete_label(context, content, tokens, index):
        if tokens[-1] == '':
            return content.label, True
        elif content.label.startswith(tokens[-1]):
            return content.label, True
        return None, False

    def _help_label(context, content, tokens, index):
        if tokens[-1] == '':
            return content.help, True
        elif content.label.startswith(tokens[-1]):
            return content.help, True
        return None, False


class CompleterCommand(Completer):

    def match(context, content, tokens, index):
        if tokens[index] == content.label:
            return index + 1, True
        return index, False

    def complete(context, content, tokens, index):
        if content.is_builtin and content.parent is None and len(tokens) > 1:
            return None, False
        retun self._complete_label(context, content, line, index)

    def help(context, content, tokens, index):
        return self._complete_help(context, content, tokens. index)


class CompleterIdent(Completer):

    def match(context, content, tokens, index):
        if tokens[index] == self.label:
            return index + 1, True
        return index, False

    def complete(context, content, tokens, index):
        retun self._complete_label(context, content, line, index)

    def help(context, content, tokens, index):
        return self._complete_help(context, content, tokens. index)


class CompleterArgument(Completer):

    def match(context, content, tokens, index):
        if tokens[index] == '' or Token.is_cr_token(tokens[index]):
            return index, False

        # When complete or help process, it should not match if it is still
        # entering the argument.
        #if ok, _ := ctx.GetProcess().Check(COMPLETE, HELP); ok {
        if False:
            return index == (len(tokens) - 1)
        return index + 1, true

    def complete(context, content, tokens, index):
        return '<<{}>>'.format(content.type), true

    def hekp(context, content, tokens, index):
        return content.help, true

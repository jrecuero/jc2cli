from jc2cli.syntax.content import Content
from jc2cli.syntax.tokens import Token
from jc2cli.syntax.completer import CompleterSink


_CR = None


class ContentJoint(Content):

    def __init__(self, label, _help, completer=None):
        super(ContentJoint, self).__init__(label, _help, completer)
        self.matchable = False

    def is_joint(self):
        return True

    def get_str_type(self):
        return 'J'


def get_cr():
    global _CR
    if _CR is None:
        _CR = ContentJoint(Token.CR, 'Carrier return', CompleterSink())
        _CR.matchable = True
    return _CR

import jc2cli.parser.scanner as Scanner
import jc2cli.parser.token as Token


class Syntax(object):

    def __init__(self):
        self.command = None
        self.arguments = []
        self.tokens = []


class Buffer(object):

    def __init__(self):
        self.token = None
        self.literal = None
        self.size = 0


class Parser(object):

    def __init__(self):
        self.scanner = Scanner.Scanner()
        self.buffer = Buffer()

    def parse():
        syntax = Syntax()
        tok, lit = self.scan_ignore_white_space()
        if tok != Token.IDENT:
            return None, "found {0} expected command\n".format(lit)
        syntax.command = lit
        while True:
            tok, lit = self.scan_ignore_white_space()
            if tok == Token.ILLEGAL:
                return None, "found {0}, expected argument\n".format(lit)
            else if tok == Token.EOF:
                break
            syntax.arguments.append(lit)
            syntax.tokens.append(tok)
        return syntax, None

    def scan():
        if self.buffer.size:
            self.buffer.size = 0
            return (self.buffer.token, self.buffer.literal)

        self.buffer.token, self.buffer.literal = self.scanner.scan()
        return

    def scan_ignore_white_space():
        tok, lit = self.scan()
        if tok == Token.WS:
            tok, lit = self.scan()
        return

    def unscan():
        self.buffer.size = 1

import jc2cli.parser.lex.cli.lexer as Lexer
from jc2cli.parser.parser import Parser


class CommandSyntax:

    def __init__(self, command_str):
        self.string = command_str
        self.lexer = Lexer.Lexer()
        self.parser = Parser(self.lexer)
        self.graph = None
        self._done = False

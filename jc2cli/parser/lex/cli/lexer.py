import jc2cli.parser.token as Token
import jc2cli.parser.parser as BaseParser


# OPENBRACKET token [. #3
OPENBRACKET = Token.CUSTOM
# CLOSEBRACKET token ]. #4
CLOSEBRACKET = Token.CUSTOM + 1
# PIPE token |. #5
PIPE = Token.CUSTOM + 2
# ASTERISK token *. #6
ASTERISK = Token.CUSTOM + 2
# PLUS token +. #7
PLUS = Token.CUSTOM + 4
# QUESTION mark token ?. #8
QUESTION = Token.CUSTOM + 5
# ADMIRATION mark token !. #9
ADMIRATION = Token.CUSTOM + 6
# AT token @. #10
AT = Token.CUSTOM + 7
# OPENMARK token <. #11
OPENMARK = Token.CUSTOM + 8
# CLOSEMARK token >. #12
CLOSEMARK = Token.CUSTOM + 9


class Lexer(object):

    def __init__(self):
        self.syntax = BaseParser.Syntax()
        self._char_map = {'[': OPENBRACKET,
                          ']': CLOSEBRACKET,
                          '|': PIPE,
                          '*': ASTERISK,
                          '+': PLUS,
                          '?': QUESTION,
                          '!': ADMIRATION,
                          '@': AT,
                          '<': OPENMARK,
                          '>': CLOSEMARK, }

    def parse(self, index, token, lit):
        if index == 1:
            assert token == Token.IDENT, 'token:{} is not IDENT:{}'.format(token, Token.IDENT)
            self.syntax.command = lit
        else:
            self.syntax.arguments.append(lit)
            self.syntax.tokens.append(token)
        return

    def result(self):
        return self.syntax

    def get_char_map(self):
        return self._char_map

    def get_ident_chars(self):
        return ['_', '-']

    def is_ident_char(self, ch, scanner):
        return scanner.is_letter(ch) or scanner.is_digit(ch) or ch in self.get_ident_chars()

    def is_ident_prefix_char(self, ch, scanner):
        return scanner.is_letter(ch)

import jc2cli.parser.token as Token


class Scanner(object):

    def __init__(self):
        self.reader = None

    def read(self):
        ch = self.reader.read_char()
        return ch

    def unread(self):
        self.reader.unread_char()

    def is_white_space(self, ch):
        return ch in [' ', '\t', '\n']

    def is_letter(self, ch):
        return ch.isalpha(self)

    def is_digit(self, ch):
        return ch.isnumeric()

    def scan(self):
        pass

    def scan_white_space(self):
        buff.write_char(self.read())
        while True:
            ch = self.read()
            if ch == Token.EOF:
                break
            else if self.is_white_space(ch):
                self.unread()
                break
            else:
                buff.write_char(ch)
        return (Token.WS, buff.to_string())

    def scan_ident(self):
        buff.write_char(self.read())
        while True:
            ch = self.read()
            if ch == Token.EOF:
                break
            else if not self.is_letter(ch) and not self.is_digit(ch) and ch not in ['_', '-']:
                self.unread()
                break
            else:
                buff.write_char(ch)
        return (Token.IDENT, buff.to_string())

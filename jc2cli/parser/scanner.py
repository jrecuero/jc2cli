'''scanner module provides all character scanning functionality in order to
scan any lexical languages.

version: 2.0
'''

import jc2cli.parser.token as Token


class Reader(object):

    def __init__(self, line):
        self.line = line
        self.hook = 0

    def read_char(self):
        if self.hook == len(self.line):
            return Token.EOF
        char = self.line[self.hook]
        self.hook += 1
        return char

    def unread_char(self):
        self.hook -= 1


class Buffer(object):

    def __init__(self):
        self.data = None

    def write_char(self, ch):
        if self.data is None:
            self.data = ch
        else:
            self.data += ch

    def to_string(self):
        return self.data


class Scanner(object):

    def __init__(self, char_map, line=None):
        self.char_map = char_map
        self.reader = None if line is None else Reader(line)

    def set_reader(self, line):
        self.reader = Reader(line)

    def read(self):
        ch = self.reader.read_char()
        return ch

    def unread(self):
        self.reader.unread_char()

    def is_white_space(self, ch):
        return ch in [' ', '\t', '\n']

    def is_letter(self, ch):
        return ch.isalpha()

    def is_digit(self, ch):
        return ch.isdigit()

    def scan(self):
        ch = self.read()

        if ch == 0:
            return Token.EOF, ch
        elif self.is_white_space(ch):
            self.unread()
            return self.scan_white_space()
        elif self.is_letter(ch):
            self.unread()
            return self.scan_ident()

        if ch in self.char_map:
            return self.char_map[ch], ch

        return Token.ILLEGAL, ch

    def scan_white_space(self):
        buff = Buffer()
        buff.write_char(self.read())
        while True:
            ch = self.read()
            if ch == Token.EOF:
                break
            elif not self.is_white_space(ch):
                self.unread()
                break
            else:
                buff.write_char(ch)
        return (Token.WS, buff.to_string())

    def scan_ident(self):
        buff = Buffer()
        buff.write_char(self.read())
        while True:
            ch = self.read()
            if ch == Token.EOF:
                break
            elif not self.is_letter(ch) and not self.is_digit(ch) and ch not in ['_', '-']:
                self.unread()
                break
            else:
                buff.write_char(ch)
        return (Token.IDENT, buff.to_string())

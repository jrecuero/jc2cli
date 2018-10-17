'''test_parser module test parser version 2.0.

version: 2.0
'''

import pytest
from jc2cli.parser.parser import Parser, new_syntax
import jc2cli.parser.token as Token
import jc2cli.parser.lex.cli.lexer as Lexer


@pytest.fixture
def parser(request):
    lexer = Lexer.Lexer()
    return Parser(lexer)


def test_parser_new_parser(parser):
    assert parser.buffer is not None
    assert parser.buffer.token is None
    assert parser.buffer.literal is None
    assert parser.buffer.size == 0


def test_parser_unscan(parser):
    parser.unscan()
    assert parser.buffer.size == 1


@pytest.mark.parametrize(('inputs', 'results'),
                         [('SELECT table', (Token.IDENT, 'SELECT')),
                          ('[data]', (Lexer.OPENBRACKET, '[')),
                          ('  table', (Token.WS, '  ')), ])
def test_parser_scan(parser, inputs, results):
    parser.set_line(inputs)
    got = parser.scan()
    assert got == results


@pytest.mark.parametrize(('inputs', 'results'),
                         [('SELECT table', (Token.IDENT, 'SELECT')),
                          ('[data]', (Lexer.OPENBRACKET, '[')),
                          ('  table', (Token.IDENT, 'table')), ])
def test_parser_scan_ignore_white_space(parser, inputs, results):
    parser.set_line(inputs)
    got = parser.scan_ignore_white_space()
    assert got == results


@pytest.mark.parametrize(('inputs', 'results'),
                         [('SELECT table', new_syntax('SELECT', ['table'], [Token.IDENT])),
                          ('SELECT [table]?', new_syntax('SELECT',
                                                         ['[', 'table', ']', '?'],
                                                         [Lexer.OPENBRACKET, Token.IDENT, Lexer.CLOSEBRACKET, Lexer.QUESTION])), ])
def test_parser_parse(parser, inputs, results):
    parser.set_line(inputs)
    got, error = parser.parse()
    assert got is not None
    assert error is None
    assert got.command == results.command
    assert got.arguments == results.arguments
    assert got.tokens == results.tokens

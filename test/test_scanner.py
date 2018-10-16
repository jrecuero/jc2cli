'''test_scanner module test scanner version 2.0.

version: 2.0
'''

import pytest
from jc2cli.parser.scanner import Scanner
import jc2cli.parser.token as Token


@pytest.fixture
def scanner(request):
    char_map = {'[': Token.OPENBRACKET,
                ']': Token.CLOSEBRACKET,
                '|': Token.PIPE,
                '*': Token.ASTERISK,
                '+': Token.PLUS,
                '?': Token.QUESTION,
                '!': Token.ADMIRATION,
                '@': Token.AT,
                '<': Token.OPENMARK,
                '>': Token.CLOSEMARK, }
    return Scanner(char_map)


@pytest.mark.parametrize(('inputs', 'results'),
                         [('SELECT table', 'SELECT table'), ])
def test_scanner_read(scanner, inputs, results):
    scanner.set_reader(inputs)
    for i in range(len(inputs)):
        got = scanner.read()
        assert got == results[i]


@pytest.mark.parametrize(('inputs', 'results'),
                         [('SELECT table', 'SELECT table'), ])
def test_scanner_unread(scanner, inputs, results):
    scanner.set_reader(inputs)
    for i in range(len(inputs)):
        scanner.read()
        scanner.unread()
    for i in range(len(inputs)):
        got = scanner.read()
        assert got == results[i]


@pytest.mark.parametrize(('inputs', 'results'),
                         [('A B\tC\nD', [False, True, False, True, False, True, False]), ])
def test_scanner_is_whitespace(scanner, inputs, results):
    scanner.set_reader(inputs)
    for i, c in enumerate(inputs):
        got = scanner.is_white_space(c)
        assert got == results[i], 'fail for {}:{}'.format(i, c)


@pytest.mark.parametrize(('inputs', 'results'),
                         [('A B\tC\nD', [True, False, True, False, True, False, True]), ])
def test_scanner_is_letter(scanner, inputs, results):
    scanner.set_reader(inputs)
    for i, c in enumerate(inputs):
        got = scanner.is_letter(c)
        assert got == results[i], 'fail for {}:{}'.format(i, c)


@pytest.mark.parametrize(('inputs', 'results'),
                         [('A 1B\t2C\n3D4', [False, False, True, False, False, True, False, False, True, False, True]), ])
def test_scanner_is_digit(scanner, inputs, results):
    scanner.set_reader(inputs)
    for i, c in enumerate(inputs):
        got = scanner.is_digit(c)
        assert got == results[i], 'fail for {}:{}'.format(i, c)


@pytest.mark.parametrize(('inputs', 'results'),
                         [('   Data', (Token.WS, '   ')), ])
def test_scanner_scan_white_space(scanner, inputs, results):
    scanner.set_reader(inputs)
    got = scanner.scan_white_space()
    assert got == results, 'fail {} vs {}'.format(got, results)


@pytest.mark.parametrize(('inputs', 'results'),
                         [('SELECT', (Token.IDENT, 'SELECT')), ])
def test_scanner_scan_ident(scanner, inputs, results):
    scanner.set_reader(inputs)
    got = scanner.scan_ident()
    assert got == results, 'fail {} vs {}'.format(got, results)


@pytest.mark.parametrize(('inputs', 'results'),
                         [('SELECT', (Token.IDENT, 'SELECT')),
                          ('[DATA]', (Token.OPENBRACKET, '[')), ])
def test_scanner_scan(scanner, inputs, results):
    scanner.set_reader(inputs)
    got = scanner.scan()
    assert got == results, 'fail {} vs {}'.format(got, results)

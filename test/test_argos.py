import pytest
from jc2cli.decorators import command, argo
from jc2cli.builtin.argos import Str, Int, Enum, Range, Constant, Line, Dicta
from jc2cli.namespace import Handler
from jc2cli.error_handler import CliError, CliValidationError


NAMESPACE = 'test.test_argos'


def _quoted(st):
    return '"{}"'.format(st) if ' ' in st else st


@pytest.fixture(params=[NAMESPACE])
def cli_call(request):
    namespace = request.param
    h = Handler()
    h.create_namespace(namespace)
    h.context.root.switch_to(namespace)
    return h.get_namespace(namespace).cli.exec_user_input


#
# Test command without Enum argument
@command('COMMAND-ONE val')
@argo('val', Enum(['alpha', 'beta', 'omega']), None)
def do_command_one(val):
    return 'cONE {}'.format(val)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-ONE alpha', 'cONE alpha'),
                          ('COMMAND-ONE beta', 'cONE beta'),
                          ('COMMAND-ONE omega', 'cONE omega'), ])
def test_command_one_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-ONE',
                          'COMMAND-ONE gamma',
                          'COMMAND-ONE ALPHA', ])
def test_command_one_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command without Range argument
@command('COMMAND-TWO val')
@argo('val', Range([[1, 50], [52, 54, 56], [60, 100], ]), None)
def do_command_two(val):
    return 'cTWO {}'.format(val)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-TWO 1', 'cTWO 1'),
                          ('COMMAND-TWO 25', 'cTWO 25'),
                          ('COMMAND-TWO 50', 'cTWO 50'),
                          ('COMMAND-TWO 52', 'cTWO 52'),
                          ('COMMAND-TWO 54', 'cTWO 54'),
                          ('COMMAND-TWO 56', 'cTWO 56'),
                          ('COMMAND-TWO 60', 'cTWO 60'),
                          ('COMMAND-TWO 80', 'cTWO 80'),
                          ('COMMAND-TWO 100', 'cTWO 100'), ])
def test_command_two_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-TWO',
                          'COMMAND-TWO 0',
                          'COMMAND-TWO 51',
                          'COMMAND-TWO 55',
                          'COMMAND-TWO 59',
                          'COMMAND-TWO 101', ])
def test_command_two_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command without Int argument
@command('COMMAND-THREE val')
@argo('val', Int(), None)
def do_command_three(val):
    return 'cTHREE {}'.format(val)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-THREE 0', 'cTHREE 0'),
                          ('COMMAND-THREE 1', 'cTHREE 1'),
                          ('COMMAND-THREE 100', 'cTHREE 100'), ])
def test_command_three_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-THREE',
                          'COMMAND-THREE alpha',
                          'COMMAND-THREE one1',
                          'COMMAND-THREE 1one', ])
def test_command_three_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command without Str argument
@command('COMMAND-FOUR val')
@argo('val', Str(), None)
def do_command_four(val):
    return 'cFOUR {}'.format(_quoted(val))


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-FOUR hello', 'cFOUR hello'),
                          ('COMMAND-FOUR 1', 'cFOUR 1'),
                          ('COMMAND-FOUR "hello world"', 'cFOUR "hello world"'), ])
def test_command_four_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-FOUR', ])
def test_command_four_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command without Constant argument
@command('COMMAND-FIVE value')
@argo('value', Constant(), 'value')
def do_command_five(value):
    return 'cFIVE {}'.format(value)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-FIVE value', 'cFIVE value'), ])
def test_command_five_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-FIVE',
                          'COMMAND-FIVE other',
                          'COMMAND-FIVE VALUE', ])
def test_command_five_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command without Line argument
@command('COMMAND-SIX line')
@argo('line', Line(), None)
def do_command_six(line):
    return 'cSIX {}'.format(line)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-SIX value', 'cSIX value'),
                          ('COMMAND-SIX hello world', 'cSIX hello world'),
                          ('COMMAND-SIX', 'cSIX '), ])
def test_command_six_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


#
# Test command without Dicta argument
@command('COMMAND-SEVEN [dicta]@')
@argo('dicta', Dicta(), {})
def do_command_seven(dicta):
    return 'cSEVEN {}'.format(dicta)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-SEVEN id=0', "cSEVEN {'id': '0'}"),
                          ('COMMAND-SEVEN id=1 key=2', "cSEVEN {'id': '1', 'key': '2'}"), ])
def test_command_seven_ok(cli_call, commands, results):
    result = cli_call(commands, reraise=True)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-SEVEN',
                          'COMMAND-SEVEN one',
                          'COMMAND-SEVEN id=1 one',
                          'COMMAND-SEVEN one id=1',
                          'COMMAND-SEVEN one id=1 one', ])
def test_command_seven_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)

import pytest
from jc2cli.decorators import command, argo
from jc2cli.builtin.argos import Str, Int, Dicta
from jc2cli.namespace import Handler
from jc2cli.error_handler import CliError, CliValidationError


NAMESPACE = 'test.test_syntax'


def _quoted(st):
    return '"{}"'.format(st) if ' ' in st else st


@pytest.fixture(params=[NAMESPACE])
def cli_call(request):
    h = Handler()
    return h.create_cli_for_namespace(request.param)


#
# Test Unknow command
@pytest.mark.parametrize('commands', ['COMMAND-ZERO'])
def test_unknown_fail(cli_call, commands):
    with pytest.raises(CliError):
        cli_call(commands, reraise=True)


#
# Test command without arguments
@command('COMMAND-ONE')
def do_command_one():
    return 'cONE'


@pytest.mark.parametrize(('commands', 'results'), [('COMMAND-ONE', 'cONE')])
def test_command_one_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-ONE one'])
def test_command_one_fail(cli_call, commands):
    with pytest.raises(CliError):
        cli_call(commands, reraise=True)


#
# Test command with one string mandatory argument
@command('COMMAND-TWO name')
@argo('name', Str(), None)
def do_command_two(name):
    return 'cTWO {0}'.format(_quoted(name))


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-TWO one', 'cTWO one'),
                          ('COMMAND-TWO "one and two"', 'cTWO "one and two"')])
def test_command_two_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-TWO',
                                      'COMMAND-TWO one two'])
def test_command_two_fail(cli_call, commands):
    with pytest.raises(CliError):
        cli_call(commands, reraise=True)


#
# Test command with one integer mandatory argument
@command('COMMAND-THREE number')
@argo('number', Int(), None)
def do_command_three(number):
    return 'cTHREE {0}'.format(number)


@pytest.mark.parametrize(('commands', 'results'), [('COMMAND-THREE 0', 'cTHREE 0'),
                                                   ('COMMAND-THREE -1', 'cTHREE -1'),
                                                   ('COMMAND-THREE 100', 'cTHREE 100'), ])
def test_command_three_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-THREE',
                                      'COMMAND-THREE one'])
def test_command_three_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with two mandatory arguments one integer and one string
@command('COMMAND-FOUR name number')
@argo('name', Str(), None)
@argo('number', Int(), None)
def do_command_four(name, number):
    return 'cFOUR {0} {1}'.format(_quoted(name), number)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-FOUR one 1', 'cFOUR one 1'),
                          ('COMMAND-FOUR "test zero" 0', 'cFOUR "test zero" 0'),
                          ('COMMAND-FOUR negative -1', 'cFOUR negative -1'), ])
def test_command_four_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-FOUR',
                          'COMMAND-FOUR 1',
                          'COMMAND-FOUR one',
                          'COMMAND-FOUR two one', ])
def test_command_four_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with one optional (zero-or-one) string parameter
@command('COMMAND-FIVE [name]?')
@argo('name', Str(), 'none')
def do_command_five(name):
    return 'cFIVE {0}'.format(_quoted(name))


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-FIVE', 'cFIVE none'),
                          ('COMMAND-FIVE -name one', 'cFIVE one'),
                          ('COMMAND-FIVE -name "one and two"', 'cFIVE "one and two"'), ])
def test_command_five_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-FIVE -name',
                                      'COMMAND-FIVE one',
                                      'COMMAND-FIVE one two',
                                      'COMMAND-FIVE -name one two', ])
def test_command_five_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with one mandatory integer parameer and one optional
# (zero-or-one) string parameter
@command('COMMAND-SIX name [number]?')
@argo('name', Str(), None)
@argo('number', Int(), 0)
def do_command_six(name, number):
    return 'cSIX {0} {1}'.format(_quoted(name), number)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-SIX one', 'cSIX one 0'),
                          ('COMMAND-SIX one -number 1', 'cSIX one 1'),
                          ('COMMAND-SIX "negative one" -number -1', 'cSIX "negative one" -1'), ])
def test_command_six_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-SIX one -number one',
                                      'COMMAND-SIX two -number',
                                      'COMMAND-SIX -number 3',
                                      'COMMAND-SIX four 4', ])
def test_command_six_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with one mandatory argument and two conditional optional
# arguments
@command('COMMAND-SEVEN fname [lname | age]?')
@argo('fname', Str(), None)
@argo('lname', Str(), 'none')
@argo('age', Int(), 0)
def do_command_seven(fname, lname, age):
    return 'cSEVEN {0} {1} {2}'.format(_quoted(fname), _quoted(lname), age)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-SEVEN one', 'cSEVEN one none 0'),
                          ('COMMAND-SEVEN two -lname TWO', 'cSEVEN two TWO 0'),
                          ('COMMAND-SEVEN three -age 30', 'cSEVEN three none 30'), ])
def test_command_seven_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-SEVEN one -lname ONE -age 1'])
def test_command_seven_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with one optional (zero or more) argument
@command('COMMAND-EIGHT [name]*')
@argo('name', Str(), 'none')
def do_command_eight(name):
    return 'cEIGHT {0}'.format(name)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-EIGHT', 'cEIGHT none'),
                          ('COMMAND-EIGHT -name one', 'cEIGHT one'),
                          ('COMMAND-EIGHT -name one -name two', "cEIGHT ['one', 'two']"), ])
def test_command_eight_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-EIGHT -name',
                                      'COMMAND-EIGHT -name one -name', ])
def test_command_eight_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with one mandatory argument and two condional optional
# (zero-or-more) arguments
@command('COMMAND-NINE name [age | zipi]*')
@argo('name', Str(), None)
@argo('age', Int(), 0)
@argo('zipi', Int(), 900)
def do_command_nine(name, age, zipi):
    return 'cNINE {0} {1} {2}'.format(name, age, zipi)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-NINE one', 'cNINE one 0 900'),
                          ('COMMAND-NINE two -age 2', 'cNINE two 2 900'),
                          ('COMMAND-NINE three -zipi 903', 'cNINE three 0 903'),
                          ('COMMAND-NINE four -age 4 -zipi 904', 'cNINE four 4 904'),
                          ('COMMAND-NINE five -age 50 -age 51', 'cNINE five [50, 51] 900'),
                          ('COMMAND-NINE six -zipi 960 -zipi 961', 'cNINE six 0 [960, 961]'),
                          ('COMMAND-NINE seven -age 70 -age 71 -zipi 907', 'cNINE seven [70, 71] 907'),
                          ('COMMAND-NINE eight -age 8 -zipi 980 -zipi 981', 'cNINE eight 8 [980, 981]'),
                          ('COMMAND-NINE nine -age 90 -age 91 -zipi 990 -zipi 991', 'cNINE nine [90, 91] [990, 991]'),
                          ('COMMAND-NINE ten -zipi 910 -age 10', 'cNINE ten 10 910'),
                          ])
def test_command_nine_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-NINE one -age',
                          'COMMAND-NINE two -age 2 -age',
                          'COMMAND-NINE three -zipi',
                          'COMMAND-NINE four -zipi 93 -zipi',
                          'COMMAND-NINE five -age -zipi',
                          'COMMAND-NINE six -age -zipi 96',
                          'COMMAND-NINE seven -age -age',
                          'COMMAND-NINE eight -zipi -zipi', ])
def test_command_nine_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with two condional optional (zero-or-more) arguments
@command('COMMAND-TEN [age | zipi]*')
@argo('age', Int(), 0)
@argo('zipi', Int(), 900)
def do_command_ten(age, zipi):
    return 'cTEN {0} {1}'.format(age, zipi)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-TEN', 'cTEN 0 900'),
                          ('COMMAND-TEN -age 2', 'cTEN 2 900'),
                          ('COMMAND-TEN -zipi 903', 'cTEN 0 903'),
                          ('COMMAND-TEN -age 4 -zipi 904', 'cTEN 4 904'),
                          ('COMMAND-TEN -age 50 -age 51', 'cTEN [50, 51] 900'),
                          ('COMMAND-TEN -zipi 960 -zipi 961', 'cTEN 0 [960, 961]'),
                          ('COMMAND-TEN -age 70 -age 71 -zipi 907', 'cTEN [70, 71] 907'),
                          ('COMMAND-TEN -age 8 -zipi 980 -zipi 981', 'cTEN 8 [980, 981]'),
                          ('COMMAND-TEN -age 90 -age 91 -zipi 990 -zipi 991', 'cTEN [90, 91] [990, 991]'), ])
def test_command_ten_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-TEN -age',
                          'COMMAND-TEN -age 2 -age',
                          'COMMAND-TEN -zipi',
                          'COMMAND-TEN -zipi 93 -zipi',
                          'COMMAND-TEN -age -zipi',
                          'COMMAND-TEN -age -zipi 96',
                          'COMMAND-TEN -age -age',
                          'COMMAND-TEN -zipi -zipi', ])
def test_command_ten_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with one optional (onre or more) argument
@command('COMMAND-ELEVEN [name]+')
@argo('name', Str(), 'none')
def do_command_eleven(name):
    return 'cELEVEN {0}'.format(name)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-ELEVEN -name one', 'cELEVEN one'),
                          ('COMMAND-ELEVEN -name one -name two', "cELEVEN ['one', 'two']"), ])
def test_command_eleven_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands', ['COMMAND-ELEVEN',
                                      'COMMAND-ELEVEN -name',
                                      'COMMAND-ELEVEN -name one -name', ])
def test_command_eleven_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with two condional optional (one-or-more) arguments
@command('COMMAND-TWELVE [age | zipi]+')
@argo('age', Int(), 0)
@argo('zipi', Int(), 900)
def do_command_twelve(age, zipi):
    return 'cTWELVE {0} {1}'.format(age, zipi)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-TWELVE -age 2', 'cTWELVE 2 900'),
                          ('COMMAND-TWELVE -zipi 903', 'cTWELVE 0 903'),
                          ('COMMAND-TWELVE -age 4 -zipi 904', 'cTWELVE 4 904'),
                          ('COMMAND-TWELVE -age 50 -age 51', 'cTWELVE [50, 51] 900'),
                          ('COMMAND-TWELVE -zipi 960 -zipi 961', 'cTWELVE 0 [960, 961]'),
                          ('COMMAND-TWELVE -age 70 -age 71 -zipi 907', 'cTWELVE [70, 71] 907'),
                          ('COMMAND-TWELVE -age 8 -zipi 980 -zipi 981', 'cTWELVE 8 [980, 981]'),
                          ('COMMAND-TWELVE -age 90 -age 91 -zipi 990 -zipi 991', 'cTWELVE [90, 91] [990, 991]'),
                          ('COMMAND-TWELVE -zipi 910 -age 10', 'cTWELVE 10 910'), ])
def test_command_twelve_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-TWELVE',
                          'COMMAND-TWELVE -age',
                          'COMMAND-TWELVE -age 2 -age',
                          'COMMAND-TWELVE -zipi',
                          'COMMAND-TWELVE -zipi 93 -zipi',
                          'COMMAND-TWELVE -age -zipi',
                          'COMMAND-TWELVE -age -zipi 96',
                          'COMMAND-TWELVE -age -age',
                          'COMMAND-TWELVE -zipi -zipi', ])
def test_command_twelve_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with free form argument
@command('COMMAND-THIRTEEN name [desc]@')
@argo('name', Str(), None)
@argo('desc', Str(), 'none')
def do_command_thirteen(name, desc):
    return 'cTHIRTEEN {0} {1}'.format(name, desc)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-THIRTEEN one ONE', 'cTHIRTEEN one ONE'),
                          ('COMMAND-THIRTEEN two TWO 2', "cTHIRTEEN two ['TWO', '2']"),
                          ('COMMAND-THIRTEEN three THREE x=3', "cTHIRTEEN three ['THREE', 'x=3']"),
                          ('COMMAND-THIRTEEN four y=4 FOUR', "cTHIRTEEN four ['y=4', 'FOUR']"),
                          ('COMMAND-THIRTEEN five x=FIVE y=5', "cTHIRTEEN five ['x=FIVE', 'y=5']"), ])
def test_command_thirteen_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-THIRTEEN zero', ])
def test_command_thirteen_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with free form argument as dictionary
@command('COMMAND-FOURTEEN name [desc]@')
@argo('name', Str(), None)
@argo('desc', Dicta(), {})
def do_command_fourteen(name, desc):
    return 'cFOURTEEN {0} {1}'.format(name, desc)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-FOURTEEN one x=ONE', "cFOURTEEN one {'x': 'ONE'}"),
                          ('COMMAND-FOURTEEN two x=TWO y=2', "cFOURTEEN two {'x': 'TWO', 'y': '2'}"), ])
def test_command_fourteen_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-FOURTEEN zero',
                          'COMMAND-FOURTEEN one ONE',
                          'COMMAND-FOURTEEN two x=TWO 2',
                          'COMMAND-FOURTEEN three THREE y=3', ])
def test_command_fourteen_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with mandatory argument and a constant argument
@command('COMMAND-FIFTEEN name <key>')
@argo('name', Str(), None)
@argo('key', Str(), None)
def do_command_fifteen(name, key):
    return 'cFIFTEEN {0} {1}'.format(name, key)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-FIFTEEN one key', 'cFIFTEEN one key'), ])
def test_command_fifteen_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-FIFTEEN one',
                          'COMMAND-FIFTEEN one other', ])
def test_command_fifteen_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with mandatory argument and a conditional mandatory
# two constant argument
@command('COMMAND-SIXTEEN name [<key1> | <key2>]!')
@argo('name', Str(), None)
@argo('key1', Str(), 'none')
@argo('key2', Str(), 'none')
def do_command_sixteen(name, key1, key2):
    return 'cSIXTEEN {0} {1} {2}'.format(name, key1, key2)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-SIXTEEN one key1', 'cSIXTEEN one key1 none'),
                          ('COMMAND-SIXTEEN two key2', 'cSIXTEEN two none key2'), ])
def test_command_sixteen_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-SIXTEEN one',
                          'COMMAND-SIXTEEN one other',
                          'COMMAND-SIXTEEN one key1 key2',
                          'COMMAND-SIXTEEN one key1 other',
                          'COMMAND-SIXTEEN one other key2', ])
def test_command_sixteen_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)


#
# Test command with mandatory argument and a conditional mandatory
# two arguments
@command('COMMAND-SEVENTEEN name [age | zipi]!')
@argo('name', Str(), None)
@argo('age', Int(), 0)
@argo('zipi', Int(), 900)
def do_command_seventenn(name, age, zipi):
    return 'cSEVENTEEN {0} {1} {2}'.format(name, age, zipi)


@pytest.mark.parametrize(('commands', 'results'),
                         [('COMMAND-SEVENTEEN one -age 1', 'cSEVENTEEN one 1 900'),
                          ('COMMAND-SEVENTEEN two -zipi 902', 'cSEVENTEEN two 0 902'), ])
def test_command_seventeen_ok(cli_call, commands, results):
    result = cli_call(commands)
    assert result == results


@pytest.mark.parametrize('commands',
                         ['COMMAND-SEVENTEEN one',
                          'COMMAND-SEVENTEEN two -age 2 -zipi 902', ])
def test_command_seventeen_fail(cli_call, commands):
    with pytest.raises((CliError, CliValidationError)):
        cli_call(commands, reraise=True)

import pytest
from jc2cli.namespace import Handler
from jc2cli.decorators import icommand, argo
from jc2cli.builtin.argos import Str


NAMESPACE = 'test.test_decorator'


@pytest.fixture(params=[NAMESPACE])
def namespace_handler(request):
    h = Handler()
    return h.get_ns_handler_after_create_and_switch(request.param)


#
# Test icommand without arguments
@icommand('COMMAND-ONE')
def do_command_one(ns_handler):
    return 'cONE ' + ns_handler.context.command_one


@pytest.mark.parametrize(('commands', 'context', 'results'),
                         [('COMMAND-ONE', 'command-one', 'cONE ')])
def test_command_one_ok(namespace_handler, commands, context, results):
    namespace_handler.context.command_one = context
    result = namespace_handler.cli.exec_user_input(commands)
    assert result == results + context


# @pytest.mark.parametrize('commands', ['COMMAND-ONE one'])
# def test_command_one_fail(namespace_handler, commands):
#     with pytest.raises(CliError):
#         namespace_handler(commands, reraise=True)


#
# Test icommand with one Str argument
@icommand('COMMAND-TWO name')
@argo('name', Str(), 0)
def do_command_two(ns_handler, name):
    return 'cTWO {} '.format(name) + ns_handler.context.command_two


@pytest.mark.parametrize(('commands', 'context', 'results'),
                         [('COMMAND-TWO two', 'command-two', 'cTWO two ')])
def test_command_two_ok(namespace_handler, commands, context, results):
    namespace_handler.context.command_two = context
    result = namespace_handler.cli.exec_user_input(commands)
    assert result == results + context

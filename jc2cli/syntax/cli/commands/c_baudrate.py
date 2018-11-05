from jc2cli.syntax.cli.command import argo
from jc2cli.syntax.cli.commands.c_set import c_set


@c_set.command('BAUDRATE rate')
@argo('rate')
def c_baudrate(**kwargs):
    print('baudrate: {}'.format(kwargs.get('rate')))

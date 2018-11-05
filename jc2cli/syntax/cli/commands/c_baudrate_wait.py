from jc2cli.syntax.cli.command import argo
from jc2cli.syntax.cli.commands.c_baudrate import c_baudrate


@c_baudrate.command('WAIT timeout')
@argo('timeout')
def c_wait(**kwargs):
    print('wait: {}'.format(kwargs.get('timeout')))

from jc2cli.syntax.cli.command import argo
from jc2cli.syntax.cli.commands.c_speed import c_speed


@c_speed.command('WAIT timeout')
@argo('timeout')
def c_wait(**kwargs):
    print('wait: {}'.format(kwargs.get('timeout')))

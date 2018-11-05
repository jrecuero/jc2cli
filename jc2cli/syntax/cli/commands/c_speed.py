from jc2cli.syntax.cli.command import argo
from jc2cli.syntax.cli.commands.c_set import c_set


@c_set.command('SPEED speed')
@argo('speed')
def c_speed(**kwargs):
    print('speed: {}'.format(kwargs.get('speed')))

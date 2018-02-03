from jc2cli.decorators import command, mode, argo
from jc2cli.argo_types import Str, Int


@command('START app default')
@argo('app', Str, "none")
@argo('default', Str)
def start(app, default):
    print('start: running in main module with {0} and {1}'.format(app, default))
    return True


@command("END time")
@argo('time', Int, 0)
def end():
    print('end: running in main module')
    return True


@mode("CLI", "examples.main.Cli")
def cli():
    return True


class Cli(object):

    def __init__(self):
        pass

    @command('START app default')
    @argo('app', Str, "none")
    @argo('default', Str)
    def start(self):
        print('start: running in main module main.Cli class')
        return True

    @command("END time")
    @argo('time', Int, 0)
    def end(self):
        print('end: running in main module main.Cli class')
        return True

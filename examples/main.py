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
def end(time):
    print('end: running in main module at {0}'.format(time))
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
    def start(self, app, default):
        print('start: running in main module main.Cli class with {0} and {1}'.format(app, default))
        return True

    @command("END time")
    @argo('time', Int, 0)
    def end(self, time):
        print('end: running in main module main.Cli class at {0}'.format(time))
        return True

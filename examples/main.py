from jc2cli.decorators import command, mode, argo


@command('START app default')
@argo('app', str, "none")
@argo('default', str)
def start():
    print('start: running in main module')
    return True


@command("END time")
@argo('time', int, 0)
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
    @argo('app', str, "none")
    @argo('default', str)
    def start(self):
        print('start: running in main module main.Cli class')
        return True

    @command("END time")
    @argo('time', int, 0)
    def end(self):
        print('end: running in main module main.Cli class')
        return True

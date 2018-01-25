from jc2cli.decorators import command, argo


@command('START app default')
@argo('app', str, "none")
@argo('default', str)
def start():
    print('start: running in main module')


@command("END time")
@argo('time', int, 0)
def end():
    print('end: running in main module')


class Cli(object):

    def __init__(self):
        pass

    @command('START app default')
    @argo('app', str, "none")
    @argo('default', str)
    def start(self):
        print('start: running in main module main.Cli class')

    @command("END time")
    @argo('time', int, 0)
    def end(self):
        print('end: running in main module main.Cli class')

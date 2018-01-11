from decorators import command, argo


@command('START app default')
@argo('app', str, "none")
@argo('default', str)
def start():
    print('start')


@command("END time")
@argo('time', int, 0)
def end():
    print('end')


class Cli(object):

    def __init__(self):
        pass

    @command('START app default')
    @argo('app', str, "none")
    @argo('default', str)
    def start(self):
        print('cli start')

    @command("END time")
    @argo('time', int, 0)
    def end(self):
        print('cli end')

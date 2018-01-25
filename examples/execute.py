from jc2cli.decorators import command, argo


@command("START time", 'New')
@argo('time', int, 0)
def start():
    print('config start: runnning in execute module')


class Cli(object):

    def __init__(self):
        pass

    @command("EXEC time")
    @argo('time', int, 0)
    def execute(self):
        print('exec: running in execute module execute.Cli class')

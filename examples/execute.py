from jc2cli.decorators import command, argo
from jc2cli.argo_types import Int


@command("START time", namespace='New')
@argo('time', Int(), 0)
def start():
    print('config start: runnning in execute module renamed to New')


class Cli(object):

    def __init__(self):
        pass

    @command("EXEC time")
    @argo('time', Int(), 0)
    def execute(self):
        print('exec: running in execute module execute.Cli class')

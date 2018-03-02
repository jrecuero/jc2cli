from jc2cli.decorators import command, argo
from jc2cli.builtin.argos import Int
import jc2cli.tools.loggerator as loggerator

MODULE = 'EX.WORK.execute'
logger = loggerator.getLoggerator(MODULE)


@command("START time", namespace='New')
@argo('time', Int(), 0)
def start():
    logger.display('config start: runnning in execute module renamed to New')


class Cli(object):

    def __init__(self):
        pass

    @command("EXEC time")
    @argo('time', Int(), 0)
    def execute(self):
        logger.display('exec: running in execute module execute.Cli class')

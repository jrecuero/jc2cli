from jc2cli.decorators import command, argo
from jc2cli.builtin.argos import Str, Int
import jc2cli.tools.loggerator as loggerator

MODULE = 'EX.WORK.balances'
logger = loggerator.getLoggerator(MODULE)


@command('MOVE steps direction')
@argo('steps', Int(help='Steps to move'), None)
@argo('direction', Str(help='Direction to move'), None)
def do_move(steps, direction):
    logger.display('move: {} steps to {}'.format(steps, direction))
    return True


class Balanced(object):

    def __init__(self):
        pass

    @command("GET obj")
    @argo('obj', Str(), None)
    def do_get(self, obj):
        logger.display('[{}] get: {}'.format(self, obj))
        return True

from jc2cli.decorators import command, argo
from jc2cli.builtin.argos import Str, Int
import jc2cli.tools.loggerator as loggerator

MODULE = 'EX.WORK.classy'
logger = loggerator.getLoggerator(MODULE)


class Cli(object):

    def __init__(self):
        pass

    @command('MOVE steps direction')
    @argo('steps', Int(help='Steps to move'), None)
    @argo('direction', Str(help='Direction to move'), None)
    def do_move(self, steps, direction):
        logger.display('[{}] move: {} steps to {}'.format(self, steps, direction))
        return True

    @command("GET obj")
    @argo('obj', Str(), None)
    def do_get(self, obj):
        logger.display('[{}] get: {}'.format(self, obj))
        return True

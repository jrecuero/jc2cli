from jc2cli.decorators import command, argo
from jc2cli.argo_types import Str
import jc2cli.tools.loggerator as loggerator

MODULE = 'EXAMPLES.WORK.config'
logger = loggerator.getLoggerator(MODULE)


class Cli(object):

    def __init__(self):
        pass

    @command('CONFIG app default')
    @argo('app', Str(), "none")
    @argo('default', Str(), "none")
    def config(self):
        logger.display('config: running in config module')

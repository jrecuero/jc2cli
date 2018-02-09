from jc2cli.decorators import command, argo
from jc2cli.argo_types import Str


class Cli(object):

    def __init__(self):
        pass

    @command('CONFIG app default')
    @argo('app', Str(), "none")
    @argo('default', Str(), "none")
    def config(self):
        print('config: running in config module')

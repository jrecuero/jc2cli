from decorators import command, argo


class Cli(object):

    def __init__(self):
        pass

    @command('CONFIG app default')
    @argo('app', str, "none")
    @argo('default', str)
    def config(self):
        print('config')

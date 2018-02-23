import os
from jc2cli.decorators import command, argo
from jc2cli.namespace import Handler
from jc2cli.builtin.argos import Str
import jc2cli.tools.loggerator as loggerator

MODULE = 'EXAMPLES.WORK.local_run'
logger = loggerator.getLoggerator(MODULE)


@command('COMMAND app default')
@argo('app', Str(help='Enter app name'), "none")
@argo('default', Str(help='Enter default value'), "none")
def do_command(app, default):
    logger.display('COMMAND: "{0}" "{1}"'.format(app, default))
    return True


class RunCli(object):

    def __init__(self):
        mm = __file__
        namespace = mm[:-3].replace(os.sep, '.')
        __import__(namespace)
        handler = Handler()
        handler.create_namespace(namespace)
        handler.switch_and_run_namespace(namespace)


if __name__ == '__main__':
    RunCli()

from functools import partial
from jc2cli.namespace import Handler
from jc2cli.default.handlers import handler_mode, handler_none


class RunCli(object):

    def __init__(self):
        __import__('examples.work.main')
        # __import__('examples.work.config')
        # __import__('examples.work.execute')

        handler = Handler()
        handler.create_namespace('cli',
                                 ns_module='examples.work.main.Cli',
                                 handler=handler_none,
                                 with_class_defaults=True)
        handler.create_namespace('main',
                                 ns_module='examples.work.main',
                                 handler=partial(handler_mode, handler.get_namespace('cli')),
                                 with_defaults=True)
        handler.switch_and_run_namespace('main')


if __name__ == '__main__':

    # import sys
    # import os
    # sys.path.append(os.path.join('/Users/jorecuer', 'Repository/winpdb-1.4.8'))
    # import rpdb2
    # rpdb2.start_embedded_debugger("jrecuero")

    RunCli()

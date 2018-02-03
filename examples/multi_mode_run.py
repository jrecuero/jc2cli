from functools import partial
from jc2cli.tree import Tree
from jc2cli.base import Base
from jc2cli.namespace import Handler
from jc2cli.default.handlers import handler_mode, handler_none
from jc2cli.default.commands import extend_with_defaults, extend_with_class_defaults


class RunCli(object):

    def __init__(self):
        __import__('examples.main')
        # __import__('examples.config')
        # __import__('examples.execute')

        self.modes = {}
        self.modes['main.cli'] = Handler('examples.main.Cli', handler=handler_none)
        self.modes['main.cli'].start_commands()
        self.modes['main.cli'].create_cli()
        self.modes['main'] = Handler('examples.main', handler=partial(handler_mode, self.modes['main.cli']))
        self.modes['main'].start_commands()
        self.modes['main'].create_cli()
        extend_with_class_defaults('examples.main.Cli')
        extend_with_defaults('examples.main')

        self.modes['main'].switch_and_run()

    def handler(self, command, *args, **kwargs):
        line = kwargs.get('line')
        command, _ = Base.get_command_from_line(line)
        if command == 'exit':
            return False
        elif command == 'cli':
            self.modes['main.cli'].switch_and_run()
        else:
            Tree.run(command, *args, **kwargs)
        return True

    def handler_none(self, command, *args, **kwargs):
        # if command == 'exit':
        #     self.modes['main'].switch_to()
        #     return False
        # else:
        #     Tree.run_none(command, *args, **kwargs)
        #     return True
        return Tree.run_none(command, *args, **kwargs)


if __name__ == '__main__':

    # import sys
    # import os
    # sys.path.append(os.path.join('/Users/jorecuer', 'Repository/winpdb-1.4.8'))
    # import rpdb2
    # rpdb2.start_embedded_debugger("jrecuero")

    RunCli()

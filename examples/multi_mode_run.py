from jc2cli.tree import Tree
from jc2cli.base import Base
from jc2cli.namespace import Handler
from jc2cli.default.handlers import handler_mode


class RunCli(object):

    def __init__(self):
        __import__('examples.main')
        # __import__('examples.config')
        # __import__('examples.execute')

        self.modes = {}
        self.modes['main'] = Handler('examples.main', handler=handler_mode)
        self.modes['main'].start_commands()
        self.modes['main'].create_cli()
        self.modes['main.cli'] = Handler('examples.main.Cli', handler=self.handler_none)
        self.modes['main.cli'].start_commands()
        self.modes['main.cli'].create_cli()

        self.modes['main'].switch_and_run()

    def handler(self, line):
        command, _ = Base.get_command_from_line(line)
        if command == 'exit':
            return False
        elif command == 'cli':
            self.modes['main.cli'].switch_and_run()
        else:
            Tree.run(command)
        return True

    def handler_none(self, line):
        command, _ = Base.get_command_from_line(line)
        if command == 'exit':
            self.modes['main'].switch_to()
            return False
        else:
            Tree.run_none(command)
            return True


if __name__ == '__main__':
    RunCli()

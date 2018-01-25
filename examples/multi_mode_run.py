from jc2cli.tree import Tree
from jc2cli.base import Base


class RunCli(object):

    def __init__(self):
        __import__('examples.main')
        __import__('examples.config')
        __import__('examples.execute')

        self.modes = {}
        self.modes['main'] = {'cli': None,
                              'namespace': 'examples.main',
                              'ns_module': 'examples.main',
                              'handler': self.handler}
        self.modes['main.cli'] = {'cli': None,
                                  'namespace': 'examples.main.Cli',
                                  'ns_module': 'examples.main.Cli',
                                  'handler': self.handler_none}

        active_commands = Tree.start(self.modes['main']['namespace'],
                                     self.modes['main']['ns_module'])
        self.modes['main']['cli'] = Base(self.modes['main']['namespace'],
                                         active_commands,
                                         self.modes['main']['handler'])
        active_commands = Tree.start(self.modes['main.cli']['namespace'],
                                     self.modes['main.cli']['ns_module'])
        self.modes['main.cli']['cli'] = Base(self.modes['main.cli']['namespace'],
                                             active_commands,
                                             self.modes['main.cli']['handler'])
        Tree.switch_to(self.modes['main']['namespace'])
        self.modes['main']['cli'].run()

    def handler(self, line):
        command, _ = Base.get_command_from_line(line)
        if command == 'exit':
            return False
        elif command == 'cli':
            Tree.switch_to(self.modes['main.cli']['namespace'])
            self.modes['main.cli']['cli'].run()
        else:
            Tree.run(command)
        return True

    def handler_none(self, line):
        command, _ = Base.get_command_from_line(line)
        if command == 'exit':
            Tree.switch_to(self.modes['main']['namespace'])
            return False
        else:
            Tree.run_none(command)
            return True


if __name__ == '__main__':
    RunCli()

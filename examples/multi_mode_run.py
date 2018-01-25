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
        base = Base(self.modes['main']['namespace'],
                    active_commands,
                    self.modes['main']['handler'])
        base.run()

    def handler(self, line):
        if line == 'exit':
            return False
        elif line == 'cli':
            active_commands = Tree.start(self.modes['main.cli']['namespace'],
                                         self.modes['main.cli']['ns_module'])
            base = Base(self.modes['main.cli']['namespace'],
                        active_commands,
                        self.modes['main.cli']['handler'])
            base.run()
        else:
            Tree.run(line)
        return True

    def handler_none(self, line):
        if line == 'exit':
            Tree.switch_to(self.modes['main']['namespace'])
            return False
        else:
            Tree.run_none(line)
            return True


if __name__ == '__main__':
    RunCli()

from jc2cli.tree import Tree
from jc2cli.base import Base


# MAIN = __import__('examples.main')
# __import__('examples.config')
# __import__('examples.execute')


class RunCli(object):

    def __init__(self):
        __import__('examples.main')
        __import__('examples.config')
        __import__('examples.execute')

        # for k, v in Tree.root().get_db().items():
        #     print('{0} : {1}'.format(k, v))
        # main = Tree.start('examples.main')
        # for k, v in main.items():
        #     print('{0} : {1}'.format(k, v.name))
        #     Tree.run(k)
        # cli = Tree.start('examples.main.Cli')
        # for k, v in cli.items():
        #     print('{0} : {1}'.format(k, v.name))
        #     # It is required to pass a parameter, because these commands
        #     # are class methods and they require a class instance to be
        #     # passed.
        #     # Tree.run(k, None)
        #     Tree.run_none(k)

        self.commands = Tree.start('examples.main.Cli', 'examples.main.Cli')
        base = Base('examples.main.Cli', self.commands, self.handler)
        base.run()

    def handler(self, line):
        Tree.run_none(line)
        return True


if __name__ == '__main__':
    # for k, v in Tree.root().get_db().items():
    #     print('{0} : {1}'.format(k, v))
    # main = Tree.start('examples.main')
    # for k, v in main.items():
    #     print('{0} : {1}'.format(k, v.name))
    #     v.command.cb()
    # cli = Tree.start('examples.main.Cli')
    # for k, v in cli.items():
    #     print('{0} : {1}'.format(k, v.name))
    #     v.command.cb(MAIN.main.Cli())
    #     v.command.cb(None)
    RunCli()

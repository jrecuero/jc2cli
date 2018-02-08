from jc2cli.tree import Tree
from jc2cli.decorators import command, help


@command('exit')
def do_exit():
    return False


@command('syntax')
@help('Display syntax for all commands.')
def do_syntax():
    for node_instance in Tree.command_tree().values():
        print(node_instance.command.syntax)
    return True


@command('help')
@help('Display this help information.')
def do_help():
    for command_name, node_instance in Tree.command_tree().items():
        print('{0} : {1}'.format(command_name, node_instance.command.help))
    return True


class Defaults(object):

        @command('exit')
        def do_exit(self):
            return do_exit()

        @command('syntax')
        @help('Display syntax for all commands.')
        def do_syntax(self):
            return do_syntax()

        @command('help')
        @help('Display this help information.')
        def do_help(self):
            return do_help()


def defaults_namespace():
    return 'jc2cli.default.commands'


def class_defaults_namespace():
    return 'jc2cli.default.commands.Defaults'

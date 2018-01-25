from jc2cli.decorators import command
from jc2cli.tree import Tree


@command('exit')
def exit():
    return False


class Defaults(object):

        @command('exit')
        def exit(self):
            return False


def extend_with_defaults(namespace):
    Tree.extend(namespace, 'jc2cli.default.commands')


def extend_with_class_defaults(namespace):
    Tree.extend(namespace, 'jc2cli.default.commands.Defaults')

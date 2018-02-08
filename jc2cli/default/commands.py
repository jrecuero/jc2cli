from jc2cli.decorators import command


@command('exit')
def exit():
    return False


class Defaults(object):

        @command('exit')
        def exit(self):
            return False


def defaults_namespace():
    return 'jc2cli.default.commands'


def class_defaults_namespace():
    return 'jc2cli.default.commands.Defaults'

import os
import importlib


class CLI:

    def __init__(self):
        self.last_command = None
        self.commands = []

    def import_commands(self, base_dir):
        files = os.listdir(base_dir)
        base_mod = base_dir.replace('/', '.')
        for mod in ['{}.{}'.format(base_mod, f[:-3]) for f in files if f.startswith('c_')]:
            print('loading module {}...'.format(mod))
            importlib.import_module(mod)

    def append(self, command):
        self.last_command = command
        self.commands.append(command)
        print('create command "{}"'.format(command.dn))

    def append_argo(self, label):
        print('create argo "{}" for "{}"'.format(label, self.last_command.dn))
        self.last_command.argos.append(label)


def cli():
    try:
        return cli.instance
    except AttributeError:
        print('create mycli instance')
        cli.instance = CLI()
        return cli.instance


def command(syntax, parent=None):
    cli().append(Command(syntax, parent))

    def f_command(f):
        cli().last_command.cb = f
        return cli().last_command
    return f_command


def argo(label, **kwargs):

    def f_argo(f):
        cli().append_argo(label)
        return f
    return f_argo


class Command:

    def __init__(self, syntax, parent=None, cb=None):
        self.syntax = syntax
        self.label = syntax.split()[0]
        self.parent = parent
        self.cb = cb
        self.argos = []
        self.dn = '{}{}'.format('{}.'.format(parent.dn) if parent else '', self.label)

    def command(self, syntax):
        return command(syntax, self)

    # def __call__(self, **kwargs):
    #     return self.cb(**kwargs)

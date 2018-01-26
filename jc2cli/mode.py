from jc2cli.command import Command


class Mode(Command):

    def __init__(self, cb):
        super(Mode, self).__init__(cb)
        self.namespace = None

from jc2cli.namespace import Handler


# MAIN = __import__('examples.main')
# __import__('examples.config')
# __import__('examples.execute')


class RunCli(object):

    def __init__(self):
        __import__('examples.main')
        # __import__('examples.config')
        # __import__('examples.execute')

        handler = Handler()
        handler.create_namespace('examples.main')
        handler.switch_and_run_namespace('examples.main')


if __name__ == '__main__':
    RunCli()

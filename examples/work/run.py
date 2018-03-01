from jc2cli.namespace import Handler


# MAIN = __import__('examples.work.main')
# __import__('examples.work.config')
# __import__('examples.work.execute')


class RunCli(object):

    def __init__(self):
        __import__('examples.work.main')
        # __import__('examples.work.config')
        # __import__('examples.work.execute')

        handler = Handler()
        handler.create_namespace('examples.work.main')
        handler.switch_and_run_namespace('examples.work.main', rprompt='<RUN>')


if __name__ == '__main__':
    RunCli()

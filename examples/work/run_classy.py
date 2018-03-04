from jc2cli.namespace import Handler
from examples.work.classy import Cli


class RunCli(object):

    def __init__(self):
        module = 'examples.work.classy'
        ns_module = 'examples.work.classy.Cli'
        __import__(module)

        handler = Handler()
        handler.create_namespace(ns_module,
                                 is_class_cmd=True)
        handler.switch_and_run_cli_for_namespace(ns_module, rprompt='<CLASSY>')


class RunCli2(object):

    def __init__(self):
        module = 'examples.work.classy'
        ns_module = 'examples.work.classy.Cli'
        __import__(module)
        handler = Handler()
        handler.create_namespace(ns_module,
                                 class_cmd_obj=Cli())
        handler.switch_and_run_cli_for_namespace(ns_module, rprompt='<CLASSY>')


if __name__ == '__main__':
    # RunCli()
    RunCli2()

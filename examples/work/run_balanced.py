from jc2cli.namespace import Handler
from examples.work.classy import Cli


class RunCli(object):

    def __init__(self):
        module = 'examples.work.balanced'
        ns_module = 'examples.work.balanced.Balanced'
        namespace = 'balanced'
        # __import__(module)
        handler = Handler()
        handler.create_namespace(namespace,
                                 module=module,
                                 ns_module=ns_module,
                                 import_ns=True,
                                 class_cmd_obj=Cli())
        handler.switch_and_run_cli_for_namespace(namespace, rprompt='<BALANCED>')


class RunCli2(object):

    def __init__(self):
        """It will include commands from examples.work.balanced and from
        examples.work.balanced.Balanced.
        """
        module = 'examples.work.balanced'
        ns_module = 'examples.work.balanced'
        namespace = 'balanced'
        # __import__(module)
        handler = Handler()
        handler.create_namespace(namespace,
                                 module=module,
                                 ns_module=ns_module,
                                 import_ns=True,
                                 matched=False,
                                 class_cmd_obj=Cli())
        handler.switch_and_run_cli_for_namespace(namespace, rprompt='<BALANCED>')


class RunCli3(object):

    def __init__(self):
        module = 'examples.work'
        ns_module = 'examples.work'
        namespace = 'work'
        __import__('examples.work.main')
        __import__('examples.work.balanced')
        handler = Handler()
        handler.create_namespace(namespace,
                                 module=module,
                                 ns_module=ns_module,
                                 matched=True)
        handler.switch_and_run_cli_for_namespace(namespace, rprompt='<BALANCED>')


if __name__ == '__main__':
    # RunCli()
    # RunCli2()
    RunCli3()

from functools import partial
from jc2cli.namespace import Handler
from jc2cli.builtin.handlers import handler_mode, handler_none


def right_prompt(cli):
    # right_prompt.counter = getattr(right_prompt, 'counter', 0)
    # right_prompt.counter += 1
    # return ' <{}>'.format(right_prompt.counter)
    from jc2cli.tree import Tree
    if Tree.command_to_run:
        return Tree.command_to_run.syntax
    return ""


class RunCli(object):

    def __init__(self):
        __import__('examples.work.main')
        # __import__('examples.work.config')
        # __import__('examples.work.execute')

        handler = Handler()
        handler.create_namespace('cli',
                                 ns_module='examples.work.main.Cli',
                                 handler=handler_none,
                                 is_class_cmd=True)
        handler.create_namespace('main',
                                 ns_module='examples.work.main',
                                 handler=partial(handler_mode, handler.get_ns_handler('cli')))
        # handler.switch_and_run_cli_for_namespace('main', prompt='multi-run > ', rprompt=right_prompt)
        handler.switch_and_run_cli_for_namespace('main', prompt='multi-run > ')
        # handler.switch_and_run_cli_for_namespace('main', prompt='multi-run > ', rprompt='')


if __name__ == '__main__':

    # import sys
    # import os
    # sys.path.append(os.path.join('/Users/jorecuer', 'Repository/winpdb-1.4.8'))
    # import rpdb2
    # rpdb2.start_embedded_debugger("jrecuero")

    RunCli()

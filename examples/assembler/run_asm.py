__docformat__ = 'restructuredtext en'


# -----------------------------------------------------------------------------
#  _                            _
# (_)_ __ ___  _ __   ___  _ __| |_ ___
# | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
# | | | | | | | |_) | (_) | |  | |_\__ \
# |_|_| |_| |_| .__/ \___/|_|   \__|___/
#             |_|
# -----------------------------------------------------------------------------
#
from jc2cli.namespace import Handler
from examples.assembler.asm import get_cpu
from examples.assembler.executor import Executor
import jc2cli.tools.loggerator as loggerator


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'EX.ASM.run_asm'
logger = loggerator.getLoggerator(MODULE)


# -----------------------------------------------------------------------------
#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
# -----------------------------------------------------------------------------
#
def right_prompt(cli):
    st = ""
    for r, d in get_cpu().regs():
        st += ('{}: {}\n'.format(r, d))
    return st


# -----------------------------------------------------------------------------
#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
# -----------------------------------------------------------------------------
#
class RunAsmCli(object):

    def __init__(self):
        # module = 'examples.assembler.asm'
        # namespace = module
        __import__('examples.assembler.asm')
        __import__('examples.assembler.executor')
        self.namespace = 'examples.assembler'
        self.handler = Handler()

        # import sys
        # import os
        # sys.path.append(os.path.join('/Users/jorecuer', 'Repository/winpdb-1.4.8'))
        # import rpdb2
        # rpdb2.start_embedded_debugger("jrecuero")

        self.handler.create_namespace(self.namespace, matched=False)
        self.cli = self.handler.get_ns_handler(self.namespace).cli

    def run(self):
        self.handler.switch_and_run_cli_for_namespace(self.namespace,
                                                      rprompt=right_prompt,
                                                      pre_prompt='\nASM ASSEMBLER',
                                                      post_prompt='CPU READY...')


# -----------------------------------------------------------------------------
#                  _
#  _ __ ___   __ _(_)_ __
# | '_ ` _ \ / _` | | '_ \
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|
#
# -----------------------------------------------------------------------------
#
if __name__ == '__main__':
    runner = RunAsmCli()
    executor = Executor(runner.cli)
    runner.run()

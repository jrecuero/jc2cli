from jc2cli.namespace import Handler
from examples.assembler.asm import get_cpu
import jc2cli.tools.loggerator as loggerator


MODULE = 'EX.ASM.run_asm'
logger = loggerator.getLoggerator(MODULE)


def right_prompt(cli):
    st = ""
    for r, d in get_cpu().regs():
        st += ('{}: {}\n'.format(r, d))
    return st


class RunAsmCli(object):

    def __init__(self):
        # module = 'examples.assembler.asm'
        # namespace = module
        # __import__(module)
        namespace = 'examples.assembler.asm'
        h = Handler()
        h.create_namespace(namespace)
        h.switch_and_run_cli_for_namespace(namespace,
                                           rprompt=right_prompt,
                                           pre_prompt='\nASM ASSEMBLER',
                                           post_prompt='CPU READY...')


if __name__ == '__main__':
    RunAsmCli()

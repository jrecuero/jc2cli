from jc2cli.decorators import command, argo
from jc2cli.builtin.argos import Str, Int
import jc2cli.tools.loggerator as loggerator

MODULE = 'EX.ASM.asm'
logger = loggerator.getLoggerator(MODULE)


@command('DEFM label mem')
@argo('label', Str(help='Label for memory address'), None)
@argo('mem', Str(help='Memory address'), None)
def do_def_memory(label, mem):
    logger.display('define label {} for memory address {}'.format(label, mem))
    return True


@command('DEFC label cte')
@argo('label', Str(help='Label for constant'), None)
@argo('cte', Str(help='Constant value'), None)
def do_def_cte(label, cte):
    logger.display('define label {} for constant value {}'.format(label, cte))
    return True


@command('LDM src dst')
@argo('src', Str(help='Source memory address'), None)
@argo('dst', Str(help='Destination memory address'), None)
def do_load_mem_to_mem(src, dst):
    logger.display('load memory from {} to {}'.format(src, dst))
    return True


@command('LDC cte dst')
@argo('cte', Str(help='Constant value'), None)
@argo('dst', Str(help='Destination memory address'), None)
def do_load_cte_to_mem(cte, dst):
    logger.display('load constant {} to {}'.format(cte, dst))
    return True


@command('LDMR src reg')
@argo('src', Str(help='Source memory address'), None)
@argo('reg', Str(help='Destination register'), None)
def do_load_mem_to_reg(src, reg):
    logger.display('load from memory {} to register {}'.format(src, reg))
    return True


@command('LDCR cte reg')
@argo('cte', Str(help='Constant value'), None)
@argo('reg', Str(help='Destination register'), None)
def do_load_cte_to_reg(cte, reg):
    logger.display('load from memory {} to register {}'.format(cte, reg))
    return True


@command('DISP mem [bytes]?')
@argo('mem', Str(help='Memory address'), None)
@argo('bytes', Int(help='Number of bytes'), 0)
def do_disp_memory(mem, bytes):
    logger.display('display {} bytes at memory address {}'.format(bytes, mem))
    return True

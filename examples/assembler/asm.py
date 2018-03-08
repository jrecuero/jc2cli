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
from jc2cli.decorators import command, argo
from jc2cli.builtin.argos import Str, Int, Enum
import jc2cli.tools.loggerator as loggerator
from examples.assembler.machine import Machine


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'EX.ASM.asm'
logger = loggerator.getLoggerator(MODULE)


# -----------------------------------------------------------------------------
#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
# -----------------------------------------------------------------------------
#
class Size(Enum):

    def __init__(self, **kwargs):
        super(Size, self).__init__(['B', 'W'], **kwargs)
        self.help_str = "Operation byte size"


class Register(Enum):

    def __init__(self, **kwargs):
        super(Register, self).__init__(['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8'], **kwargs)
        self.help_str = "Machine register"


# -----------------------------------------------------------------------------
#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
# -----------------------------------------------------------------------------
#
def get_cpu():
    get_cpu.machine = getattr(get_cpu, 'machine', None)
    if not get_cpu.machine:
        get_cpu.machine = Machine()
    return get_cpu.machine


@command('DEFM label mem')
@argo('label', Str(help='Label for memory address'), None)
@argo('mem', Str(help='Memory address'), None)
def do_def_memory(label, mem):
    logger.display('define label {} for memory address {}'.format(label, mem))
    cpu = get_cpu()
    cpu.defm(label, mem)
    return True


@command('DEFC label cte size')
@argo('label', Str(help='Label for constant'), None)
@argo('cte', Str(help='Constant value'), None)
@argo('size', Size(), None)
def do_def_cte(label, cte, size):
    logger.display('define label {} for constant value {} [{} bytes]'.format(label, cte, size))
    cpu = get_cpu()
    cpu.defc(label, cte)
    return True


@command('LDM src dst size')
@argo('src', Str(help='Source memory address'), None)
@argo('dst', Str(help='Destination memory address'), None)
@argo('size', Size(), None)
def do_load_mem_to_mem(src, dst, size):
    logger.display('load memory from {} to {} [{} bytes]'.format(src, dst, size))
    cpu = get_cpu()
    cpu.ldm(src, dst, size)
    return True


@command('LDC cte dst size')
@argo('cte', Str(help='Constant value'), None)
@argo('dst', Str(help='Destination memory address'), None)
@argo('size', Size(), None)
def do_load_cte_to_mem(cte, dst, size):
    logger.display('load constant {} to {} [{} size]'.format(cte, dst, size))
    cpu = get_cpu()
    cpu.ldc(cte, dst, size)
    return True


@command('LDMR src reg')
@argo('src', Str(help='Source memory address'), None)
@argo('reg', Register(), None)
def do_load_mem_to_reg(src, reg):
    logger.display('load from memory {} to register {}'.format(src, reg))
    cpu = get_cpu()
    cpu.ldmr(src, reg)
    return True


@command('LDRM reg src')
@argo('reg', Register(), None)
@argo('src', Str(help='Destination memory address'), None)
def do_load_reg_to_mem(reg, src):
    logger.display('load from register {} to memory address {}'.format(reg, src))
    cpu = get_cpu()
    cpu.ldrm(reg, src)
    return True


@command('LDCR cte reg')
@argo('cte', Str(help='Constant value'), None)
@argo('reg', Register(), None)
def do_load_cte_to_reg(cte, reg):
    logger.display('load from memory {} to register {}'.format(cte, reg))
    cpu = get_cpu()
    cpu.ldcr(cte, reg)
    return True


@command('ADDM src dst size')
@argo('src', Str(help='First memory address'), None)
@argo('dst', Str(help='Second and destination memory address'), None)
@argo('size', Size(), None)
def do_add_mem_to_mem(src, dst, size):
    logger.display('Add memory {} to {} [{} bytes]'.format(src, dst, size))
    cpu = get_cpu()
    cpu.addm(src, dst, size)
    return True


@command('ADDC cte dst size')
@argo('cte', Str(help='Constant value'), None)
@argo('dst', Str(help='Second and destination memory address'), None)
@argo('size', Size(), None)
def do_add_cte_to_mem(cte, dst, size):
    logger.display('Add constant {} to {} [{} bytes]'.format(cte, dst, size))
    cpu = get_cpu()
    cpu.addc(cte, dst, size)
    return True


@command('DISP mem [bytes]?')
@argo('mem', Str(help='Memory address'), None)
@argo('bytes', Int(help='Number of bytes'), 0)
def do_disp_memory(mem, bytes):
    logger.display('display {} bytes at memory address {}'.format(bytes, mem))
    cpu = get_cpu()
    for data in cpu.disp(mem, bytes):
        logger.display('{}'.format(data))
    return True


@command('REGS [reg]?')
@argo('reg', Str(help='Register to display'), 0)
def do_registers(reg):
    logger.display('display registers {}'.format(reg))
    cpu = get_cpu()
    for r, data in cpu.regs(reg):
        logger.display('{}: {}'.format(r, data))
    return True


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
    pass

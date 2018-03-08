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
MODULE = 'EX.ASM.machine'
logger = loggerator.getLoggerator(MODULE)

BYTE_SIZE = 256
WORD_SIZE = BYTE_SIZE * BYTE_SIZE
M_SIZE = BYTE_SIZE
R_SIZE = WORD_SIZE
MEM_SIZE = 256 * 256
MEM_BASE_ADDR = 0
DISP_SIZE = 256
DISP_BASE_ADDR = 256 * 256
REGS_SIZE = 8


# -----------------------------------------------------------------------------
#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
# -----------------------------------------------------------------------------
#


# -----------------------------------------------------------------------------
#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
# -----------------------------------------------------------------------------
#
class Memory(list):

    def __init__(self, size=MEM_SIZE, base_address=MEM_BASE_ADDR):
        super(Memory, self).__init__()
        self._size = size
        self._base_address = base_address
        for x in range(size):
            self.append(0)

    def __setitem__(self, index, value):
        if value < M_SIZE:
            return super(Memory, self).__setitem__(index, value)
        else:
            raise Exception('Value is not byte size')

    def append(self, value):
        if len(self) < self._size:
            if value < M_SIZE:
                super(Memory, self).append(value)
            else:
                raise Exception('Value is not byte size')
        else:
            raise Exception('Memory is full')

    def insert(self, index, value):
        if index < len(self):
            if value < M_SIZE:
                super(Memory, self).append(value)
            else:
                raise Exception('Value is not byte size')
        else:
            raise Exception('Memory is full')

    def ltp(self, index):
        """ltp returns the logical-to-physical memory conversion.
        """
        if self._base_address <= index < self._base_address + self._size:
            return index - self._base_address
        else:
            raise Exception('Out of the logical memory space')

    def ptl(self, index):
        """ptl returns the physical-to-logical memory conversion.
        """
        if index < self._size:
            return index + self._base_address
        else:
            raise Exception('Out of the physical memory space')


class Display(Memory):

    def __init__(self, size=DISP_SIZE, base_address=DISP_BASE_ADDR):
        super(Display, self).__init__(size, base_address)


class Registers(dict):

    def __init__(self, size=REGS_SIZE):
        super(Registers, self).__init__()
        self._size = size
        for x in range(size):
            self['R{}'.format(x + 1)] = 0

    def __getitem__(self, index):
        if isinstance(index, int):
            if 0 < index <= self._size:
                return super(Registers, self).__getitem__('R{}'.format(index))
            else:
                raise Exception('Not a valid register')
        else:
            return super(Registers, self).__getitem__(index)

    def __setitem__(self, index, value):
        if isinstance(index, int):
            if 0 < index <= self._size:
                return super(Registers, self).__setitem__('R{}'.format(index), value)
            else:
                raise Exception('Not a valid register')
        else:
            return super(Registers, self).__setitem__(index, value)


class Language(object):

    def __init__(self):
        self._cte_db = {}
        self._mem_db = {}

    def add_cte(self, label, value):
        self._cte_db[label] = int(value)

    def get_cte(self, label):
        return self._cte_db.get(label, None)

    def add_mem(self, label, address):
        self._mem_db[label] = int(address)

    def get_mem(self, label):
        return self._mem_db.get(label, None)

    def any_data(self, src):
        try:
            return int(src)
        except ValueError:
            return self.get_cte(src)

    def any_address(self, addr):
        try:
            return int(addr)
        except ValueError:
            return self.get_mem(addr)

    def any_reg(self, reg):
        try:
            index = int(reg)
            return 'R{}'.format(index)
        except ValueError:
            return reg

    def load_cte_to_mem(self, label, dst):
        src_data = self.any_data(label)
        dst_addr = self.any_address(dst)
        return src_data, dst_addr

    def load_mem_to_mem(self, addr, dst):
        src_addr = self.any_address(addr)
        dst_addr = self.any_address(dst)
        return src_addr, dst_addr

    def load_cte_to_reg(self, value, reg):
        src_data = self.any_data(value)
        dst_reg = self.any_reg(reg)
        return src_data, dst_reg

    def load_mem_to_reg(self, src, reg):
        src_addr = self.any_address(src)
        dst_reg = self.any_reg(reg)
        return src_addr, dst_reg

    def load_reg_to_mem(self, reg, dst):
        src_reg = self.any_reg(reg)
        dst_addr = self.any_address(dst)
        return src_reg, dst_addr


class Machine(object):

    def __init__(self):
        self.memory = Memory()
        self.display = Display()
        self.registers = Registers()
        self.lang = Language()

    def ldc(self, src, dst, size):
        src_data, dst_addr = self.lang.load_cte_to_mem(src, dst)
        self.memory[dst_addr] = src_data
        logger.info('ldc mem[{}] = {} /{}'.format(dst_addr, src_data, size))

    def ldm(self, src, dst, size):
        src_addr, dst_addr = self.lang.load_mem_to_mem(src, dst)
        self.memory[dst_addr] = self.memory[src_addr]
        logger.info('ldm mem[{}] = {} /{}'.format(dst_addr, self.memory[src_addr], size))

    def ldmr(self, src, reg):
        src_addr, dst_reg = self.lang.load_mem_to_reg(src, reg)
        self.registers[dst_reg] = self.memory[src_addr]
        logger.info('ldmr {} = {}'.format(dst_reg, self.memory[src_addr]))

    def ldrm(self, reg, src):
        dst_addr, src_reg = self.lang.load_mem_to_reg(src, reg)
        self.memory[dst_addr] = self.registers[src_reg]
        logger.info('ldmr mem[{}] = {}'.format(dst_addr, self.registers[src_reg]))

    def ldcr(self, src, reg):
        src_data, dst_reg = self.lang.load_cte_to_reg(src, reg)
        self.registers[dst_reg] = src_data
        logger.info('ldcr {} = {}'.format(dst_reg, src_data))

    def addm(self, src, dst, size):
        src_addr, dst_addr = self.lang.load_mem_to_mem(src, dst)
        self.memory[dst_addr] += self.memory[src_addr]
        logger.info('addm mem[{}] = {} /{}'.format(dst_addr, self.memory[dst_addr], size))

    def addc(self, src, dst, size):
        src_data, dst_addr = self.lang.load_cte_to_mem(src, dst)
        self.memory[dst_addr] += src_data
        logger.info('addc mem[{}] = {} /{}'.format(dst_addr, self.memory[dst_addr], size))

    def defm(self, label, addr):
        self.lang.add_mem(label, addr)
        logger.info('defm {} = {}'.format(label, addr))

    def defc(self, label, cte):
        self.lang.add_cte(label, cte)
        logger.info('defc {} = {}'.format(label, cte))

    def disp(self, src, bytes):
        start = self.lang.any_address(src)
        size = self.lang.any_data(bytes)
        size = size if size else 1
        end = start + size
        return self.memory[start:end]

    def regs(self, reg=None):
        if reg:
            r = self.lang.any_reg(reg)
            return [(r, self.registers[r]), ]
        else:
            return self.registers.items()


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

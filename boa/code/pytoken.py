from boa.code.version import Version
from boa.exception import ConverterException
from bytecode import Instr, UNSET, Compare, Label
from logzero import logger


class PyToken:

    instruction = None  # type:Instr
    expression = None
    index = 0

    jump_found = False

    jump_target = None
    jump_from = None
    jump_from_addr = None
    jump_to_addr = None

    is_dynamic_appcall = False

    _methodname = None

    is_breakpoint = False

    def __init__(self, instruction, expression, index, fallback_ln):
        self.instruction = instruction
        self.expression = expression
        self.index = index
        self._methodname = None
        self.jump_from = None
        self.jump_target = None
        self.jump_found = False
        self.jump_from_addr = None
        self.jump_to_addr = None
        # self.jump_to_addr_abs = None
        # self.jump_from_addr_abs = None

        if isinstance(instruction, Label):
            self.jump_target = instruction
            self.instruction = Instr("NOP", lineno=fallback_ln)
        elif isinstance(instruction.arg, Label):
            self.jump_from = instruction.arg

    @property
    def jump_to_addr_abs(self):
        if self.jump_to_addr and self.expression.container_method:
            return self.jump_to_addr + self.expression.container_method.address
        return 0

    @property
    def jump_from_addr_abs(self):
        if self.jump_from_addr and self.expression.container_method:
            return self.jump_from_addr + self.expression.container_method.address
        return 0

    @property
    def file(self):
        try:
            return self.expression.container_method.module.path
        except Exception as e:
            print("Could not get file %s " % e)
        return None

    @property
    def method_lineno(self):
        return self.expression.container_method.start_line_no - 1

    @property
    def method_name(self):
        return self.expression.container_method.name

    @property
    def lineno(self):
        return self.instruction.lineno

    @property
    def arg_str(self):
        #        print("INSTRUCTION ARG: %s %s" % (type(self.instruction.arg), self.instruction.arg))
        params = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
        if self.jump_target:
            return 'from %s' % (self.jump_from_addr_abs)
        elif self.jump_from:
            return 'to %s' % (self.jump_to_addr_abs)
        elif self._methodname:
            return '%s(%s)' % (self._methodname, ','.join(params[0:self.instruction.arg]))
        elif isinstance(self.instruction.arg, Compare):
            return self.instruction.arg.name
        elif isinstance(self.instruction.arg, bytes) or isinstance(self.instruction.arg, bytearray):
            return str(self.instruction.arg)
        return self.instruction.arg if self.instruction.arg != UNSET else ''

    @property
    def args(self):
        return self.instruction.arg

    @property
    def pyop(self):
        return self.instruction.opcode

    @property
    def func_name(self):
        if not self._methodname:
            self._methodname = self.expression.lookup_method_name(self.index)
        return self._methodname

    @property
    def num_params(self):
        return self.args

    def to_vm(self, tokenizer, prev_token=None):
        """

        :param tokenizer:
        :param prev_token:
        :return:
        """

        try:
            Version.converter.pytoken_to_vm(tokenizer, self)
        except ConverterException:
            #            import pdb
            #            pdb.set_trace()
            logger.warning("Op Not Converted %s %s %s %s %s" % (self.instruction.arg, self.instruction.name, self.method_name, self.lineno, self.method_lineno))

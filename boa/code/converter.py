import abc

from boa.code import pyop
from boa.exception import ConverterException
from boa.interop import VMOp
from bytecode import Compare


class IConverter(abc.ABC):
    @abc.abstractmethod
    def pytoken_to_vm(self, tokenizer, pytoken, prev_token=None):
        """
        Converts a python intermediary token to the corresponding neo vm opcodes
        and include them in the bytecode

        :param tokenizer: Tokenizer responsible for handling the bytecode
        :param pytoken: Python token to be converted
        :param prev_token: Previous converted python token
        """
        pass


class Neo2Converter(IConverter):
    def pytoken_to_vm(self, tokenizer, pytoken, prev_token=None):
        op = pytoken.instruction.opcode
        #        print("CONVERTING OP: %s %s " % (pytoken.instruction.name, pytoken.instruction.arg))

        if op == pyop.NOP:
            tokenizer.convert1(VMOp.NOP, pytoken)

        elif op == pyop.RETURN_VALUE:
            tokenizer.method_end_items()
            tokenizer.convert1(VMOp.RET, pytoken)

        # control flow

        elif op == pyop.JUMP_FORWARD:
            tokenizer.convert1(VMOp.JMP, pytoken, data=bytearray(2))

        elif op == pyop.JUMP_ABSOLUTE:
            tokenizer.convert1(VMOp.JMP, pytoken, data=bytearray(2))

        elif op == pyop.POP_JUMP_IF_FALSE:
            tokenizer.convert1(
                VMOp.JMPIFNOT, pytoken, data=bytearray(2))
        # JUMP_IF_FALSE_OR_POP is not supported by the VM
        # elif op == pyop.JUMP_IF_FALSE_OR_POP:
        #     tokenizer.convert_pop_jmp_if(pytoken)
        #         VMOp.JMPIFNOT, pytoken, data=bytearray(2))

        elif op == pyop.POP_JUMP_IF_TRUE:
            tokenizer.convert_pop_jmp_if(pytoken)

        # JUMP_IF_TRUE_OR_POP is not supported by the VM
        # elif op == pyop.JUMP_IF_TRUE_OR_POP:
        #     tokenizer.convert_pop_jmp_if(pytoken)
        # loops
        elif op == pyop.SETUP_LOOP:
            tokenizer.convert1(VMOp.NOP, pytoken)
        elif op == pyop.BREAK_LOOP:
            tokenizer.convert1(VMOp.JMP, pytoken, data=bytearray(2))

        elif op == pyop.POP_BLOCK:
            tokenizer.convert1(VMOp.NOP, pytoken)

        elif op == pyop.FROMALTSTACK:
            tokenizer.convert1(VMOp.FROMALTSTACK, pytoken)
        elif op == pyop.DROP:
            tokenizer.convert1(VMOp.DROP, pytoken)
        elif op == pyop.XSWAP:
            tokenizer.convert1(VMOp.XSWAP, pytoken)
        elif op == pyop.ROLL:
            tokenizer.convert1(VMOp.ROLL, pytoken)

        # loading constants ( ie 1, 2 etc)
        elif op == pyop.LOAD_CONST:
            tokenizer.convert_load_const(pytoken)

        # storing / loading local variables
        elif op in [pyop.STORE_FAST, pyop.STORE_NAME]:
            tokenizer.convert_store_local(pytoken)
        elif op == pyop.LOAD_GLOBAL:

            if pytoken.instruction.arg in pytoken.expression.container_method.scope:
                tokenizer.convert_load_local(pytoken)
            else:
                pytoken.expression.add_method(pytoken)

        elif op in [pyop.LOAD_FAST, pyop.LOAD_NAME]:
            tokenizer.convert_load_local(pytoken)

        # unary ops

        elif op == pyop.UNARY_INVERT:
            tokenizer.convert1(VMOp.INVERT, pytoken)

        elif op == pyop.UNARY_NEGATIVE:
            tokenizer.convert1(VMOp.NEGATE, pytoken)

        elif op == pyop.UNARY_NOT:
            tokenizer.convert1(VMOp.NOT, pytoken)

        #            elif op == pyop.UNARY_POSITIVE:
        # hmmm
        #                tokenizer.convert1(VMOp.ABS, pytoken)
        #                pass

        # math
        elif op in [pyop.BINARY_ADD, pyop.INPLACE_ADD]:

            # we can't tell by looking up the last token what type of item it was
            # will need to figure out a different way of concatting strings
            #                if prev_token and type(prev_token.args) is str:
            #                    tokenizer.convert1(VMOp.CAT, pytoken)
            #                else:
            tokenizer.convert1(VMOp.ADD, pytoken)

        elif op in [pyop.BINARY_SUBTRACT, pyop.INPLACE_SUBTRACT]:
            tokenizer.convert1(VMOp.SUB, pytoken)

        elif op in [pyop.BINARY_MULTIPLY, pyop.INPLACE_MULTIPLY]:
            tokenizer.convert1(VMOp.MUL, pytoken)

        elif op in [pyop.BINARY_FLOOR_DIVIDE, pyop.BINARY_TRUE_DIVIDE,
                    pyop.INPLACE_FLOOR_DIVIDE, pyop.INPLACE_TRUE_DIVIDE]:
            tokenizer.convert1(VMOp.DIV, pytoken)

        elif op in [pyop.BINARY_MODULO, pyop.INPLACE_MODULO]:
            tokenizer.convert1(VMOp.MOD, pytoken)

        elif op in [pyop.BINARY_OR, pyop.INPLACE_OR]:
            tokenizer.convert1(VMOp.OR, pytoken)

        elif op in [pyop.BINARY_AND, pyop.INPLACE_AND]:
            tokenizer.convert1(VMOp.AND, pytoken)

        elif op in [pyop.BINARY_XOR, pyop.INPLACE_XOR]:
            tokenizer.convert1(VMOp.XOR, pytoken)

        elif op in [pyop.BINARY_LSHIFT, pyop.INPLACE_LSHIFT]:
            tokenizer.convert1(VMOp.SHL, pytoken)

        elif op in [pyop.BINARY_RSHIFT, pyop.INPLACE_RSHIFT]:
            tokenizer.convert1(VMOp.SHR, pytoken)

        # compare

        elif op == pyop.COMPARE_OP:

            #            pdb.set_trace()
            if pytoken.instruction.arg == Compare.GT:
                tokenizer.convert1(VMOp.GT, pytoken)
            elif pytoken.instruction.arg == Compare.GE:
                tokenizer.convert1(VMOp.GTE, pytoken)
            elif pytoken.instruction.arg == Compare.LT:
                tokenizer.convert1(VMOp.LT, pytoken)
            elif pytoken.instruction.arg == Compare.LE:
                tokenizer.convert1(VMOp.LTE, pytoken)
            elif pytoken.instruction.arg == Compare.EQ:
                tokenizer.convert1(VMOp.EQUAL, pytoken)
            elif pytoken.instruction.arg == Compare.IS:
                tokenizer.convert1(VMOp.EQUAL, pytoken)
            elif pytoken.instruction.arg in [Compare.NE, Compare.IS_NOT]:
                tokenizer.convert1(VMOp.NUMNOTEQUAL, pytoken)
            elif pytoken.instruction.arg == Compare.IN:
                tokenizer.convert1(VMOp.SWAP, pytoken)
                tokenizer.convert1(VMOp.HASKEY, pytoken)

        # arrays
        elif op == pyop.BUILD_LIST:
            tokenizer.convert_new_array(pytoken)
        elif op == pyop.DUP_TOP:
            tokenizer.convert1(VMOp.DUP, pytoken)
        elif op == pyop.YIELD_VALUE:
            tokenizer.convert1(VMOp.REVERSE, pytoken)
        elif op == pyop.STORE_SUBSCR:
            tokenizer.convert_store_subscr(pytoken)
        elif op == pyop.BINARY_SUBSCR:
            tokenizer.convert1(VMOp.PICKITEM, pytoken)

        # dict
        elif op == pyop.BUILD_CONST_KEY_MAP:
            tokenizer.convert1(VMOp.NEWMAP, pytoken)
        elif op == pyop.BUILD_MAP:
            tokenizer.convert1(VMOp.NEWMAP, pytoken)

        elif op == pyop.BUILD_SLICE:
            tokenizer.convert_build_slice(pytoken)

        elif op in [pyop.CALL_FUNCTION, pyop.CALL_METHOD]:
            tokenizer.convert_method_call(pytoken)
        #        elif op == pyop.LOAD_METHOD:

        elif op == pyop.POP_TOP:
            pass
            # if prev_token:
            #     is_action = False
            #     for item in tokenizer.method.module.actions:
            #         if item.method_name == prev_token.func_name:
            #             is_action = True
            #
            # if is_action:
            #     tokenizer.convert1(VMOp.DROP, pytoken)

        elif op == pyop.DUP_TOP_TWO:
            tokenizer.convert_dup_top_two(pytoken)
        elif op == pyop.ROT_THREE:
            tokenizer.convert1(VMOp.ROT, pytoken)
        elif op == pyop.ROT_TWO:
            tokenizer.convert1(VMOp.SWAP)
        elif op == pyop.RAISE_VARARGS:
            pass
        #        elif op == pyop.CALL_METHOD:
        #            pass
        elif op == pyop.EXTENDED_ARG:
            tokenizer.convert1(VMOp.NOP, pytoken)
        else:
            raise ConverterException()


class Neo3Converter(IConverter):
    def pytoken_to_vm(self, tokenizer, pytoken, prev_token=None):
        # TODO: Check all the differences between Neo 2 VM and Neo 3 VM
        pass

import importlib
import sys

# Constants

PUSHINT8 = b'\x00'
PUSHINT16 = b'\x01'
PUSHINT32 = b'\x02'
PUSHINT64 = b'\x03'
PUSHINT128 = b'\x04'
PUSHINT256 = b'\x05'
PUSHA = b'\x0A'  # Convert the next four bytes to an address, and push the address onto the stack.
PUSHNULL = b'\x0B'  # The item <see langword="null"/> is pushed onto the stack.
PUSHDATA1 = b'\x0C'  # The next byte contains the number of bytes to be pushed onto the stack.
PUSHDATA2 = b'\x0D'  # The next two bytes contain the number of bytes to be pushed onto the stack.
PUSHDATA4 = b'\x0E'  # The next four bytes contain the number of bytes to be pushed onto the stack.
PUSHM1 = b'\x0F'  # The number -1 is pushed onto the stack.
PUSH0 = b'\x10'  # The number 0 is pushed onto the stack.
PUSH1 = b'\x11'  # The number 1 is pushed onto the stack.
PUSH2 = b'\x12'  # The number 2 is pushed onto the stack.
PUSH3 = b'\x13'  # The number 3 is pushed onto the stack.
PUSH4 = b'\x14'  # The number 4 is pushed onto the stack.
PUSH5 = b'\x15'  # The number 5 is pushed onto the stack.
PUSH6 = b'\x16'  # The number 6 is pushed onto the stack.
PUSH7 = b'\x17'  # The number 7 is pushed onto the stack.
PUSH8 = b'\x18'  # The number 8 is pushed onto the stack.
PUSH9 = b'\x19'  # The number 9 is pushed onto the stack.
PUSH10 = b'\x1A'  # The number 10 is pushed onto the stack.
PUSH11 = b'\x1B'  # The number 11 is pushed onto the stack.
PUSH12 = b'\x1C'  # The number 12 is pushed onto the stack.
PUSH13 = b'\x1D'  # The number 13 is pushed onto the stack.
PUSH14 = b'\x1E'  # The number 14 is pushed onto the stack.
PUSH15 = b'\x1F'  # The number 15 is pushed onto the stack.
PUSH16 = b'\x20'  # The number 16 is pushed onto the stack.


# Flow control

NOP = b'\x21'  # The <see cref="NOP"/> operation does nothing. It is intended to fill in space if opcodes are patched.
JMP = b'\x22'  # Unconditionally transfers control to a target instruction. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMP_L = b'\x23'  # Unconditionally transfers control to a target instruction. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPIF = b'\x24'  # Transfers control to a target instruction if the value is <see langword="true"/>, not <see langword="null"/>, or non-zero. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPIF_L = b'\x25'  # Transfers control to a target instruction if the value is <see langword="true"/>, not <see langword="null"/>, or non-zero. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPIFNOT = b'\x26'  # Transfers control to a target instruction if the value is <see langword="false"/>, a <see langword="null"/> reference, or zero. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPIFNOT_L = b'\x27'  # Transfers control to a target instruction if the value is <see langword="false"/>, a <see langword="null"/> reference, or zero. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPEQ = b'\x28'  # Transfers control to a target instruction if two values are equal. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPEQ_L = b'\x29'  # Transfers control to a target instruction if two values are equal. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPNE = b'\x2A'  # Transfers control to a target instruction when two values are not equal. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPNE_L = b'\x2B'  # Transfers control to a target instruction when two values are not equal. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPGT = b'\x2C'  # Transfers control to a target instruction if the first value is greater than the second value. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPGT_L = b'\x2D'  # Transfers control to a target instruction if the first value is greater than the second value. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPGE = b'\x2E'  # Transfers control to a target instruction if the first value is greater than or equal to the second value. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPGE_L = b'\x2F'  # Transfers control to a target instruction if the first value is greater than or equal to the second value. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPLT = b'\x30'  # Transfers control to a target instruction if the first value is less than the second value. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPLT_L = b'\x31'  # Transfers control to a target instruction if the first value is less than the second value. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
JMPLE = b'\x32'  # Transfers control to a target instruction if the first value is less than or equal to the second value. The target instruction is represented as a 1-byte signed offset from the beginning of the current instruction.
JMPLE_L = b'\x33'  # Transfers control to a target instruction if the first value is less than or equal to the second value. The target instruction is represented as a 4-bytes signed offset from the beginning of the current instruction.
CALL = b'\x34'  # Calls the function at the target address which is represented as a 1-byte signed offset from the beginning of the current instruction.
CALL_L = b'\x35'  # Calls the function at the target address which is represented as a 4-bytes signed offset from the beginning of the current instruction.
CALLA = b'\x36'  # Pop the address of a function from the stack, and call the function.
ABORT = b'\x37'  # It turns the vm state to FAULT immediately, and cannot be caught.
ASSERT = b'\x38'  # Pop the top value of the stack, if it false, then exit vm execution and set vm state to FAULT.
THROW = b'\x3A'
# TRY = b'\x3B'
# TRY_L = b'\x3C'
# ENDT = b'\x3D'
# ENDC = b'\x3E'
# ENDF = b'\x3F'
RET = b'\x40'  # Returns from the current method.
SYSCALL = b'\x41'  # Calls to an interop service.

# Stack

DEPTH = b'\x43'  # Puts the number of stack items onto the stack.
DROP = b'\x45'  # Removes the top stack item.
NIP = b'\x46'  # Removes the second-to-top stack item.
XDROP = b'\x48'  # The item n back in the main stack is removed.
CLEAR = b'\x49'  # Clear the stack
DUP = b'\x4A'  # Duplicates the top stack item.
OVER = b'\x4B'  # Copies the second-to-top stack item to the top.
PICK = b'\x4D'  # The item n back in the stack is copied to the top.
TUCK = b'\x4E'  # The item at the top of the stack is copied and inserted before the second-to-top item.
SWAP = b'\x50'  # The top two items on the stack are swapped.
ROT = b'\x51'  # The top three items on the stack are rotated to the left.
ROLL = b'\x52'  # The item n back in the stack is moved to the top.
REVERSE3 = b'\x53'  # Reverse the order of the top 3 items on the stack.
REVERSE4 = b'\x54'  # Reverse the order of the top 4 items on the stack.
REVERSEN = b'\x55'  # Pop the number N on the stack, and reverse the order of the top N items on the stack.

# Slot
INITSSLOT = b'\x56'  # Initialize the static field list for the current execution context.
INITSLOT = b'\x57'  # Initialize the argument slot and the local variable list for the current execution context.
LDSFLD0 = b'\x58'  # Loads the static field at index 0 onto the evaluation stack.
LDSFLD1 = b'\x59'  # Loads the static field at index 1 onto the evaluation stack.
LDSFLD2 = b'\x5A'  # Loads the static field at index 2 onto the evaluation stack.
LDSFLD3 = b'\x5B'  # Loads the static field at index 3 onto the evaluation stack.
LDSFLD4 = b'\x5C'  # Loads the static field at index 4 onto the evaluation stack.
LDSFLD5 = b'\x5D'  # Loads the static field at index 5 onto the evaluation stack.
LDSFLD6 = b'\x5E'  # Loads the static field at index 6 onto the evaluation stack.
LDSFLD = b'\x5F'  # Loads the static field at a specified index onto the evaluation stack. The index is represented as a 1-byte unsigned integer.
STSFLD0 = b'\x60'  # Stores the value on top of the evaluation stack in the static field list at index 0.
STSFLD1 = b'\x61'  # Stores the value on top of the evaluation stack in the static field list at index 1.
STSFLD2 = b'\x62'  # Stores the value on top of the evaluation stack in the static field list at index 2.
STSFLD3 = b'\x63'  # Stores the value on top of the evaluation stack in the static field list at index 3.
STSFLD4 = b'\x64'  # Stores the value on top of the evaluation stack in the static field list at index 4.
STSFLD5 = b'\x65'  # Stores the value on top of the evaluation stack in the static field list at index 5.
STSFLD6 = b'\x66'  # Stores the value on top of the evaluation stack in the static field list at index 6.
STSFLD = b'\x67'  # Stores the value on top of the evaluation stack in the static field list at a specified index. The index is represented as a 1-byte unsigned integer.
LDLOC0 = b'\x68'  # Loads the local variable at index 0 onto the evaluation stack.
LDLOC1 = b'\x69'  # Loads the local variable at index 1 onto the evaluation stack.
LDLOC2 = b'\x6A'  # Loads the local variable at index 2 onto the evaluation stack.
LDLOC3 = b'\x6B'  # Loads the local variable at index 3 onto the evaluation stack.
LDLOC4 = b'\x6C'  # Loads the local variable at index 4 onto the evaluation stack.
LDLOC5 = b'\x6D'  # Loads the local variable at index 5 onto the evaluation stack.
LDLOC6 = b'\x6E'  # Loads the local variable at index 6 onto the evaluation stack.
LDLOC = b'\x6F'  # Loads the local variable at a specified index onto the evaluation stack. The index is represented as a 1-byte unsigned integer.
STLOC0 = b'\x70'  # Stores the value on top of the evaluation stack in the local variable list at index 0.
STLOC1 = b'\x71'  # Stores the value on top of the evaluation stack in the local variable list at index 1.
STLOC2 = b'\x72'  # Stores the value on top of the evaluation stack in the local variable list at index 2.
STLOC3 = b'\x73'  # Stores the value on top of the evaluation stack in the local variable list at index 3.
STLOC4 = b'\x74'  # Stores the value on top of the evaluation stack in the local variable list at index 4.
STLOC5 = b'\x75'  # Stores the value on top of the evaluation stack in the local variable list at index 5.
STLOC6 = b'\x76'  # Stores the value on top of the evaluation stack in the local variable list at index 6.
STLOC = b'\x77'  # Stores the value on top of the evaluation stack in the local variable list at a specified index. The index is represented as a 1-byte unsigned integer.
LDARG0 = b'\x78'  # Loads the argument at index 0 onto the evaluation stack.
LDARG1 = b'\x79'  # Loads the argument at index 1 onto the evaluation stack.
LDARG2 = b'\x7A'  # Loads the argument at index 2 onto the evaluation stack.
LDARG3 = b'\x7B'  # Loads the argument at index 3 onto the evaluation stack.
LDARG4 = b'\x7C'  # Loads the argument at index 4 onto the evaluation stack.
LDARG5 = b'\x7D'  # Loads the argument at index 5 onto the evaluation stack.
LDARG6 = b'\x7E'  # Loads the argument at index 6 onto the evaluation stack.
LDARG = b'\x7F'  # Loads the argument at a specified index onto the evaluation stack. The index is represented as a 1-byte unsigned integer.
STARG0 = b'\x80'  # Stores the value on top of the evaluation stack in the argument slot at index 0.
STARG1 = b'\x81'  # Stores the value on top of the evaluation stack in the argument slot at index 1.
STARG2 = b'\x82'  # Stores the value on top of the evaluation stack in the argument slot at index 2.
STARG3 = b'\x83'  # Stores the value on top of the evaluation stack in the argument slot at index 3.
STARG4 = b'\x84'  # Stores the value on top of the evaluation stack in the argument slot at index 4.
STARG5 = b'\x85'  # Stores the value on top of the evaluation stack in the argument slot at index 5.
STARG6 = b'\x86'  # Stores the value on top of the evaluation stack in the argument slot at index 6.
STARG = b'\x87'  # Stores the value on top of the evaluation stack in the argument slot at a specified index. The index is represented as a 1-byte unsigned integer.


# Splice
NEWBUFFER = b'\x88',
MEMCPY = b'\x89',
CAT = b'\x8B'  # Concatenates two strings.
SUBSTR = b'\x8C'  # Returns a section of a string.
LEFT = b'\x8D'  # Keeps only characters left of the specified point in a string.
RIGHT = b'\x8E'  # Keeps only characters right of the specified point in a string.

# Bitwise logic
INVERT = b'\x90'  # Flips all of the bits in the input.
AND = b'\x91'  # Boolean and between each bit in the inputs.
OR = b'\x92'  # Boolean or between each bit in the inputs.
XOR = b'\x93'  # Boolean exclusive or between each bit in the inputs.
EQUAL = b'\x97'  # Returns 1 if the inputs are exactly equal, 0 otherwise.
NOTEQUAL = b'\x98'  # Returns 1 if the inputs are not equal, 0 otherwise.

# Arithmetic
SIGN = b'\x99'  # Puts the sign of top stack item on top of the main stack. If value is negative, put -1; if positive, put 1; if value is zero, put 0.
ABS = b'\x9A'  # The input is made positive.
NEGATE = b'\x9B'  # The sign of the input is flipped.
INC = b'\x9C'  # 1 is added to the input.
DEC = b'\x9D'  # 1 is subtracted from the input.
ADD = b'\x9E'  # a is added to b.
SUB = b'\x9F'  # b is subtracted from a.
MUL = b'\xA0'  # a is multiplied by b.
DIV = b'\xA1'  # a is divided by b.
MOD = b'\xA2'  # Returns the remainder after dividing a by b.
SHL = b'\xA8'  # Shifts a left b bits, preserving sign.
SHR = b'\xA9'  # Shifts a right b bits, preserving sign.
NOT = b'\xAA'  # If the input is 0 or 1, it is flipped. Otherwise the output will be 0.
BOOLAND = b'\xAB'  # If both a and b are not 0, the output is 1. Otherwise 0.
BOOLOR = b'\xAC'  # If a or b is not 0, the output is 1. Otherwise 0.
NZ = b'\xB1'  # Returns 0 if the input is 0. 1 otherwise.
NUMEQUAL = b'\xB3'  # Returns 1 if the numbers are equal, 0 otherwise.
NUMNOTEQUAL = b'\xB4'  # Returns 1 if the numbers are not equal, 0 otherwise.
LT = b'\xB5'  # Returns 1 if a is less than b, 0 otherwise.
LE = b'\xB6'  # Returns 1 if a is less than or equal to b, 0 otherwise.
GT = b'\xB7'  # Returns 1 if a is greater than b, 0 otherwise.
GE = b'\xB8'  # Returns 1 if a is greater than or equal to b, 0 otherwise.
MIN = b'\xB9'  # Returns the smaller of a and b.
MAX = b'\xBA'  # Returns the larger of a and b.
WITHIN = b'\xBB'  # Returns 1 if x is within the specified range (left-inclusive), 0 otherwise.

# Compound-type
PACK = b'\xC0'  # A value n is taken from top of main stack. The next n items on main stack are removed, put inside n-sized array and this array is put on top of the main stack.
UNPACK = b'\xC1'  # An array is removed from top of the main stack. Its elements are put on top of the main stack (in reverse order) and the array size is also put on main stack.
NEWARRAY0 = b'\xC2'  # An empty array (with size 0) is put on top of the main stack.
NEWARRAY = b'\xC3'  # A value n is taken from top of main stack. A null-filled array with size n is put on top of the main stack.
NEWARRAY_T = b'\xC4'  # A value n is taken from top of main stack. An array of type T with size n is put on top of the main stack.
NEWSTRUCT0 = b'\xC5'  # An empty struct (with size 0) is put on top of the main stack.
NEWSTRUCT = b'\xC6'  # A value n is taken from top of main stack. A zero-filled struct with size n is put on top of the main stack.
NEWMAP = b'\xC8'  # A Map is created and put on top of the main stack.
SIZE = b'\xCA'  # An array is removed from top of the main stack. Its size is put on top of the main stack.
HASKEY = b'\xCB'  # An input index n (or key) and an array (or map) are removed from the top of the main stack. Puts True on top of main stack if array[n] (or map[n]) exist, and False otherwise.
KEYS = b'\xCC'  # A map is taken from top of the main stack. The keys of this map are put on top of the main stack.
VALUES = b'\xCD'  # A map is taken from top of the main stack. The values of this map are put on top of the main stack.
PICKITEM = b'\xCE'  # An input index n (or key) and an array (or map) are taken from main stack. Element array[n] (or map[n]) is put on top of the main stack.
APPEND = b'\xCF'  # The item on top of main stack is removed and appended to the second item on top of the main stack.
SETITEM = b'\xD0'  # A value v, index n (or key) and an array (or map) are taken from main stack. Attribution array[n]=v (or map[n]=v) is performed.
REVERSEITEMS = b'\xD1'  # An array is removed from the top of the main stack and its elements are reversed.
REMOVE = b'\xD2'  # An input index n (or key) and an array (or map) are removed from the top of the main stack. Element array[n] (or map[n]) is removed.
CLEARITEMS = b'\xD3'  # Remove all the items from the compound-type.

# Types
ISNULL = b'\xD8'  # Returns true if the input is null. Returns false otherwise.
ISTYPE = b'\xD9'  # Returns true if the top item is of the specified type.
CONVERT = b'\xDB'  # Converts the top item to the specified type.

# the following is a convienience method
# for a human readable version of the ops

module = importlib.import_module('boa.interop.VMOp')
items = dir(sys.modules[__name__])


def to_name(op):
    """

    :param op:
    :return:
    """
    if isinstance(op, bytes):
        op = int.from_bytes(op, 'little')

    for item in items:
        n = getattr(module, item)

        try:
            nn = int.from_bytes(n, 'little')
            if op == nn:
                return item
        except Exception:
            pass

    return None

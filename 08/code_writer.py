from glob import glob
import sys

from setuptools import Command
from command_type import CommandType

memory_segments_map = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}


compare_op_dict = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}

compare_op_num = 0
return_label_num = 0


def get_return_label():
    global return_label_num
    label = "RETURN_LABEL{0}".format(return_label_num)
    return_label_num += 1
    return label


def push_to_stack():
    return "D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"


def pop_from_stack():
    return "@SP\nM=M-1\nA=M\nD=M"


def write_push_pop(command):
    # pop operations
    if command["command_type"] == CommandType.C_POP:
        if command["arg1"] in memory_segments_map.keys():
            line = "@{1}\nD=A\n@{0}\nA=M\nD=D+A\n@{0}\nM=D\n{2}\n@{0}\nA=M\nM=D\n@{1}\nD=A\n@{0}\nA=M\nD=A-D\n@{0}\nM=D".format(
                memory_segments_map[command["arg1"]], command["arg2"], pop_from_stack()
            )
        else:
            if command["arg1"] == "temp":
                line = "{0}\n@{1}\nM=D".format(
                    pop_from_stack(), str(command["arg2"] + 5)
                )
            elif command["arg1"] == "static":
                name = (
                    sys.argv[1].split(".vm", 1)[0].split("/")[-1]
                    + "."
                    + str(command["arg2"])
                )
                line = "{0}\n@{1}\nM=D".format(pop_from_stack(), name)
            elif command["arg1"] == "pointer":
                if command["arg2"] == 0:
                    key = "THIS"
                elif command["arg2"] == 1:
                    key = "THAT"
                line = "{0}\n@{1}\nM=D".format(pop_from_stack(), key)
    # push operations
    else:
        if command["arg1"] == "constant":
            line = "@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1".format(str(command["arg2"]))
        elif command["arg1"] in memory_segments_map.keys():
            line = "@{1}\nD=A\n@{0}\nA=M\nD=D+A\nA=D\n{2}".format(
                memory_segments_map[command["arg1"]], command["arg2"], push_to_stack()
            )
        else:
            if command["arg1"] == "temp":
                line = "@{0}\n{1}".format(str(command["arg2"] + 5), push_to_stack())
            elif command["arg1"] == "static":
                name = (
                    sys.argv[1].split(".vm", 1)[0].split("/")[-1]
                    + "."
                    + str(command["arg2"])
                )
                line = "@{0}\n{1}".format(name, push_to_stack())
            elif command["arg1"] == "pointer":
                if command["arg2"] == 0:
                    key = "THIS"
                elif command["arg2"] == 1:
                    key = "THAT"
                line = "@{0}\n{1}".format(key, push_to_stack())
    return line


def compare_operation_value(opcode):
    global compare_op_num
    line = "@TRUE{0}\nD;{1}\n@SP\nA=M\nM=0\n@END{0}\n0;JMP\n\n(TRUE{0})\n@SP\nA=M\nM=-1\n\n(END{0})\n".format(
        str(compare_op_num), compare_op_dict[opcode]
    )
    compare_op_num += 1
    return line


def write_arithmetic(command):
    opcode = "null"
    if command["arg1"] in ["eq", "lt", "gt", "sub"]:
        opcode = "D=D-M"
    elif command["arg1"] == "add":
        opcode = "D=D+M"
    elif command["arg1"] == "or":
        opcode = "D=D|M"
    elif command["arg1"] == "and":
        opcode = "D=D&M"
    elif command["arg1"] == "neg":
        opcode = "M=-M"
    elif command["arg1"] == "not":
        opcode = "M=!M"

    if command["arg1"] in ["add", "sub", "and", "or"]:
        updated_stack_value = "A=M\nM=D\n"
    elif command["arg1"] in ["eq", "lt", "gt"]:
        updated_stack_value = compare_operation_value(command["arg1"])
    elif command["arg1"] == "neg" or command["arg1"] == "not":
        updated_stack_value = "A=M\nM=-M\n"

    if command["arg1"] not in ["not", "neg"]:
        line = "@SP\nA=M\nA=A-1\nA=A-1\nD=M\nA=A+1\n{0}\n@SP\nM=M-1\nM=M-1\n{1}@SP\nM=M+1".format(
            opcode, updated_stack_value
        )
    else:
        line = "@SP\nM=M-1\nA=M\n{0}\n@SP\nM=M+1".format(opcode)
    return line


def write_goto(command):
    return "\n@{0}\n0;JMP".format(command["arg1"])


def write_if(command):
    return pop_from_stack() + "\n@{0}\nD;JNE".format(command["arg1"])


def write_label(command):
    return "({0})\n\n".format(command["arg1"])


def write_function(command):
    command_str = write_label(command)
    for i in range(1, command["arg2"]):
        command_str += write_push_pop(
            {"command_type": CommandType.C_PUSH, "arg1": "constant", "arg2": 0}
        )
        command_str += "\n"
    return command_str


def create_frame_variable():
    return "@LCL\nD=M\n@FRAME\nM=D\n\n"


def create_return_address():
    return "@5\nA=D-A\nD=M\n@RET\nM=D\n\n"


def reset_stack_pointer():
    return "@ARG\nD=M+1\n@SP\nM=D\n\n"


def reset_memory_segment_pointer(pointer):
    return "@FRAME\nD=M-1\nAM=D\nD=M\n@{0}\nM=D\n\n".format(pointer)


def write_function_return(command):
    command_str = (
        create_frame_variable()
        + create_return_address()
        + write_push_pop(
            {"command_type": CommandType.C_PUSH, "arg1": "argument", "arg2": 0}
        )
        + reset_stack_pointer()
    )
    for i in ["THAT", "THIS", "ARG", "LCL"]:
        command_str += reset_memory_segment_pointer(i)
    command_str += write_goto({"arg1": "RET"})
    return command_str


def calculate_args(nArgs):
    return "@5\nD=A\n@{0}\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n\n".format(nArgs)


def calculate_lcl():
    return "@SP\nD=M\n@LCL\nM=D\n\n"


def write_function_call(command):
    return_label = get_return_label()
    command_str = ""
    # save frame of the caller
    for i in [return_label, "LCL", "ARG", "THIS", "THAT"]:
        command_str += (
            write_push_pop(
                {"command_type": CommandType.C_PUSH, "arg1": "constant", "arg2": i}
            )
            + "\n\n"
        )
    # calculate ARG for called function
    command_str += calculate_args(command["arg2"])
    # calculate LCL for called function
    command_str += calculate_lcl()
    # mark return address
    command_str += write_label({"arg1": return_label})
    return command_str


def map_command(command):
    switcher = {
        CommandType.C_POP: write_push_pop,
        CommandType.C_PUSH: write_push_pop,
        CommandType.C_ARITHMETIC: write_arithmetic,
        CommandType.C_GOTO: write_goto,
        CommandType.C_IF: write_if,
        CommandType.C_LABEL: write_label,
        CommandType.C_FUNCTION: write_function,
        CommandType.C_RETURN: write_function_return,
        CommandType.C_CALL: write_function_call,
    }
    func = switcher.get(command["command_type"])
    return func(command)


def write_sys_init():
    return [
        "@256\nD=A\n@SP\nM=D",
        write_function_call(
            {"command_type": CommandType.C_CALL, "arg1": "Sys.init", "arg2": 0}
        ),
    ]


def write_command(command):
    asm_command = map_command(command)
    return asm_command

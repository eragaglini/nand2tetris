import re
from command_type import CommandType
from code_writer import write_command, write_sys_init

# removes all comments from input text
def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text).strip()

commands = {
    "push": CommandType.C_PUSH, 
    "pop": CommandType.C_POP, 
    "add": CommandType.C_ARITHMETIC, 
    "sub": CommandType.C_ARITHMETIC,
    "eq": CommandType.C_ARITHMETIC, 
    "lt": CommandType.C_ARITHMETIC,
    "gt": CommandType.C_ARITHMETIC,
    "and": CommandType.C_ARITHMETIC, 
    "neg": CommandType.C_ARITHMETIC,
    "not": CommandType.C_ARITHMETIC,
    "or": CommandType.C_ARITHMETIC,
    "label": CommandType.C_LABEL,
    "if-goto": CommandType.C_IF,
    "goto": CommandType.C_GOTO,
    "call": CommandType.C_CALL,
    "function": CommandType.C_FUNCTION,
    "return": CommandType.C_RETURN,
}


def command_type(c):
    return commands[c]
    

def get_command_dict(line):
    command = {}
    command["command_type"] = command_type(line[0])
    if command["command_type"] != CommandType.C_RETURN:
        if command["command_type"] == CommandType.C_ARITHMETIC:
            command["arg1"] = line[0]
        else:
            command["arg1"] = line[1]
    if command["command_type"] in [CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL]:
        command["arg2"] = int(line[2])
    return command


# parse file by path, line by line 
# create a dictionary with command data and pass it to
# code writer module
def parse_file(path):
    commands = []
    commands = write_sys_init()
    with open(path,'r',encoding = 'utf-8') as f:
        for line in f:
            line = comment_remover(line).split()
            if len(line) > 0:
                command = get_command_dict(line)
                commands.append(write_command(command))
    return commands
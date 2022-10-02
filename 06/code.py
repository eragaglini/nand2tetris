import re
from symbol_table import table, comp, dest, jump

def process_line(line):
    # if first character is @ it's an a-instruction
    if line[0] == "@":
        value = line[1:] if line[1:].isnumeric() else table[line[1:]]
        return "0" + bin(int(value))[2:].zfill(15)
        
    # c-instructions:
    else:
        if "=" in line:
            line = re.split('=|;',line)
            line = "111" + comp[line[1]] + dest[line[0]]  + (line[2] if ";" in line else "000")
        elif ";" in line:
            line = re.split(';',line)
            line = "111" + comp[line[0]] + dest["null"] + jump[line[1]]
    return line
#!/usr/bin/env python3
import sys
import os
from parser import parse_file


def main():
    if not os.path.exists(sys.argv[1]):
        print("File non esistente!")
        return

    commands = parse_file(sys.argv[1])

    file_name = sys.argv[1].split(".vm", 1)[0] + ".asm"

    with open("{}".format(file_name), "w") as file:
        for i in range(len(commands)):
            file.write(commands[i])
            if i != len(commands) - 1:
                file.write("\n\n")


if __name__ == "__main__":
    main()

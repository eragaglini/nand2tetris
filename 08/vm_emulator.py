#!/usr/bin/env python3
import sys
import os
from parser import parse_file


def main():
    if not os.path.exists(sys.argv[1]):
        print("File non esistente!")
        return

    commands = []
    path = sys.argv[1]
    if os.path.isfile(path):
        commands += parse_file(path)
        file_name = sys.argv[1].split(".vm", 1)[0] + ".asm"
    elif os.path.isdir(path):
        onlyfiles = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f)) and f.endswith(".vm")
        ]
        for f_path in onlyfiles:
            commands += parse_file(f_path)
        file_name = (
            sys.argv[1] + "/" + sys.argv[1].split(".vm", 1)[0].split("/")[1] + ".asm"
        )

    with open("{}".format(file_name), "w") as file:
        for i in range(len(commands)):
            file.write(commands[i])
            if i != len(commands) - 1:
                file.write("\n\n")


if __name__ == "__main__":
    main()

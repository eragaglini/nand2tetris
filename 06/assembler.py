#!/usr/bin/env python3
import sys
import os

from parser import parse_lines
from code import process_line
from symbol_table import update_symbol_table


def main():
    if os.path.exists(sys.argv[1]):
        file_name = sys.argv[1].split("/")[-1].split(".")[0]
    else:
        print("File non esistente!")
        return

    lines = parse_lines(sys.argv[1])
    lines = update_symbol_table(lines)

    if not os.path.exists("./bin"):
        os.mkdir("./bin")
    with open("./bin/{}.hack".format(file_name), "w") as file:
        for line in lines:
            # to print all the (relevant) lines in the file:
            file.write(process_line(line) + "\n")


if __name__ == "__main__":
    main()

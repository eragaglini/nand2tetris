#!/usr/bin/env python3
import sys
import os

import CompilationEngine


def main():
    if len(sys.argv) < 2:
        print("Error. Missing argument: input (dir./file)")
        return -1

    if not os.path.exists(sys.argv[1]):
        print("Error:", sys.argv[1], "does not exist.")
        return -1

    xml_output = False
    if len(sys.argv) > 2 and sys.argv[2] == "-xml":
        xml_output = True

    if os.path.isdir(sys.argv[1]):
        input_path = sys.argv[1]
        compile_files(input_path, xml_output)
    else:
        input_file = sys.argv[1]
        compile_file(input_file, xml_output)


def compile_file(input_path, xml_output=False):
    CompilationEngine.CompilationEngine(input_path, xml_output)


def compile_files(directory, xml_output):
    """Get all files in directory that are not .XMLs and compile them."""
    for f in os.listdir(directory):
        if f.find("jack") != -1:
            compile_file(directory + "/" + f, xml_output)


def replace_extension(input_name, extension):
    return input_name.replace(".jack", extension)


if __name__ == "__main__":
    main()

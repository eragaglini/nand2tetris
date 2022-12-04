#!/usr/bin/env python3
import sys
import os

try:
    from . import CompilationEngine
except:
    import CompilationEngine


def main():
    if len(sys.argv) < 2:
        print("Error. Missing argument: input (dir./file)")
        return -1

    if not os.path.exists(sys.argv[1]):
        print("Error:", sys.argv[1], "does not exist.")
        return -1

    if os.path.isdir(sys.argv[1]):
        input_path = sys.argv[1]
        print("Input path:", input_path)
        compile_files(input_path)
    else:
        input_file = sys.argv[1]
        compile_file(input_file, xml_output)


def compile_file(input_path):
    CompilationEngine.CompilationEngine(
        input_path,
    )


def compile_files(directory):
    """Get all files in directory that are not .XMLs and compile them."""
    for f in os.listdir(directory):
        if f.find("jack") != -1:
            compile_file(directory + "/" + f)


def replace_extension(input_name, extension):
    return input_name.replace(".jack", extension)


if __name__ == "__main__":
    main()

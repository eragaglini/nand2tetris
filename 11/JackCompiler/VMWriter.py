class VMWriter:
    def __init__(
        self,
        vmFilename=None,
    ):
        self._output = open(vmFilename, "w")

    def __del__(self):
        self._output.close()

    def write_function_signature(self, name, nLocals):
        self._output.write("function %s %d\n" % (name, nLocals))

    def write_push(self, segment, index):
        self._output.write("push {} {}\n".format(segment.lower(), index))

    def write_pop(self, segment, index):
        self._output.write("pop {} {}\n".format(segment.lower(), index))

    def write_arithmetic(self, command):
        if command == "+":
            self._output.write("add")
        elif command == "-":
            self._output.write("sub")
        elif command == "*":
            self._output.write("call Math.multiply 2")
        elif command == "/":
            self._output.write("call Math.divide 2")
        elif command == "&":
            self._output.write("and")
        elif command == "|":
            self._output.write("or")
        elif command == "<":
            self._output.write("lt")
        elif command == ">":
            self._output.write("gt")
        elif command == "=":
            self._output.write("eq")
        elif command == "~":
            self._output.write("not")
        elif command == "neg":  # Unary
            self._output.write("neg")
        self._output.write("\n")

    def write_call(self, subroutine_name, arguments):
        self._output.write("call {} {}\n".format(subroutine_name, arguments))

    def write_string(self, string):
        # we create a string object by pushing onto the stack the length of
        # the string and then by calling the string constructor with it as
        # the only argument
        self.write_push("CONSTANT", len(string))
        self.write_call("String.new", 1)
        # for every character in the string we append it
        # to the newly created string object
        for char in string:
            # https://www.geeksforgeeks.org/ord-function-python/
            # Python ord() function returns the Unicode code from a given character
            unicode_rep = ord(char)
            self.write_push("CONSTANT", unicode_rep)
            self.write_call("String.appendChar", 2)

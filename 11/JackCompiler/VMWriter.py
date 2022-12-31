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

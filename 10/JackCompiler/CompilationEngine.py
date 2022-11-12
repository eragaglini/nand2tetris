import JackTokenizer

class CompilationEngine():
    def __init__(self, inFilename, outFilename):
        self.tokenizer = JackTokenizer.JackTokenizer(inFilename)
        with open(outFilename, 'w') as outputFile:
            #outputFile.write('hello world !')
            self.compile_class()

    def compile_class():
        pass

        # to compile a class we need to start the class section
        # write the keyword, the name of the class

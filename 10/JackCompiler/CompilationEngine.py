import sys
import os
import ntpath
from xml.dom import minidom
import xml.etree.cElementTree as ET
import JackTokenizer


class CompilationEngine:
    def __init__(self, inFilename):
        self.tokenizer = JackTokenizer.JackTokenizer(inFilename)
        self.root = ET.Element("class")
        self.compile_class()
        tree = ET.ElementTree(self.root)
        outFilename = "{}/{}.xml".format(
            os.getcwd(), self.path_leaf(inFilename).rsplit(".", 1)[0]
        )
        xmlstr = minidom.parseString(ET.tostring(self.root)).toprettyxml(indent="   ")
        with open(outFilename, "w") as f:
            f.write(xmlstr)

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def _write_keyword(self, root):
        ET.SubElement(root, "keyword").text = self.tokenizer.keyword().lower()
        self.tokenizer.advance()

    def _write_identifier(self, root):
        ET.SubElement(root, "identifier").text = self.tokenizer.identifier()
        self.tokenizer.advance()

    def _write_symbol(self, root):
        symbol = self.tokenizer.symbol()
        if symbol == '"':
            symbol = "&quot;"
        if symbol == "&":
            symbol = "&amp;"
        elif symbol == "<":
            symbol = "&lt;"
        elif symbol == ">":
            symbol = "&gt;"

        ET.SubElement(root, "symbol").text = symbol
        self.tokenizer.advance()

    def _write_type(self, root):
        if self.tokenizer.token_is_primitive_type():
            self._write_keyword(root)
        else:
            self._write_identifier(root)

    def compile_var_dec(self, var_dec):
        self._write_keyword(var_dec)  # field or static or var
        self._write_type(var_dec)  # type of variable
        self._write_identifier(var_dec)  # identifier of variable

        # Are there more variables in the same line?
        while self.tokenizer.symbol() == ",":
            self._write_symbol(var_dec)
            self._write_identifier(var_dec)  # Var. name

        self._write_symbol(var_dec)  # ;

    def compile_class_var_dec(self):
        var_dec = ET.SubElement(self.root, "classVarDec")
        self.compile_var_dec(var_dec)

    def compile_parameter_list(self, parameterList):
        while not self.tokenizer.token_matches_value(')'):
            self._write_keyword(parameterList)  # Type
            self._write_identifier(parameterList)  # Name
            # More parameters?
            if self.tokenizer.symbol() == ",":
                self._write_symbol(parameterList)

    def compile_subroutine(self):
        subroutineDec = ET.SubElement(self.root, "subroutineDec")
        # function signature
        self._write_keyword(subroutineDec)  # constructor, method of function
        self._write_type(subroutineDec)  # Return type
        self._write_identifier(subroutineDec)  # subroutine identifier
        self._write_symbol(subroutineDec)  # '('

        # parameter list
        parameterList = ET.SubElement(subroutineDec, "parameterList")
        self.compile_parameter_list(parameterList)

        self._write_symbol(subroutineDec) # ')'

        # function body
        # Body:
        '''
		self._startSection("subroutineBody")
		self._writeSymbol()         # '{'

		if self.tokenizer.keyWord() == "VAR":
			self.compileVarDec() 

		if not self._tokenMatchesSymbol('}'):
			self.compileStatements()
		self._writeSymbol()         # '}' (end of subroutine body.)
		self._endSection("subroutineBody")

		self._endSection("subroutineDec")
        '''



    def compile_class(self):
        self._write_keyword(self.root)  # "Class"
        self._write_identifier(self.root)  #  className
        self._write_symbol(self.root)  # '{'

        # Variable declarations:
        while self.tokenizer.keyword().upper() in ["STATIC", "FIELD"]:
            self.compile_class_var_dec()

        # Class' subroutines declarations:
        while self.tokenizer.keyword().upper() in [
            "CONSTRUCTOR",
            "FUNCTION",
            "METHOD",
            "VOID",
        ]:
            self.compile_subroutine()

        self._write_symbol(self.root)  # '}'


def main():
    if len(sys.argv) < 2:
        print("Error. Missing argument [filename]")
        return -1
    else:
        filename = sys.argv[1]

    comp_engine = CompilationEngine(filename)


if __name__ == "__main__":
    main()

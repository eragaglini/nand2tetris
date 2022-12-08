import sys
import os
import ntpath
import xml.etree.cElementTree as ET

try:
    import JackTokenizer
    import utils
except ImportError:
    from . import JackTokenizer
    from . import utils


class CompilationEngine:
    def __init__(self, inFilename=None, xml_output=False):
        if inFilename:
            self.tokenizer = JackTokenizer.JackTokenizer(inFilename, xml_output)
            self.root = ET.Element("class")
            self.compile_class()

            if xml_output:
                outFilename = "{}/{}.xml".format(
                    os.getcwd(), self.path_leaf(inFilename).rsplit(".", 1)[0]
                )
                utils.generate_xml_file(self.root, outFilename)

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def _write_keyword(self, root):
        ET.SubElement(root, "keyword").text = self.tokenizer.keyword().lower()
        self.tokenizer.advance()

    def _write_identifier(self, root):
        ET.SubElement(root, "identifier").text = self.tokenizer.identifier()
        self.tokenizer.advance()

    def _write_integer_constant(self, root):
        ET.SubElement(root, "integerConstant").text = self.tokenizer.intVal()
        self.tokenizer.advance()

    def _write_string_constant(self, root):
        ET.SubElement(root, "stringConstant").text = self.tokenizer.stringVal()
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

    def compile_local_var_dec(self, root):
        var_dec = ET.SubElement(root, "varDec")
        if self.tokenizer.token_matches_value("var"):
            self.compile_var_dec(var_dec)

    def compile_class_var_dec(self):
        var_dec = ET.SubElement(self.root, "classVarDec")
        self.compile_var_dec(var_dec)

    def compile_parameter_list(self, parameterList):
        while not self.tokenizer.token_matches_value(")"):
            self._write_keyword(parameterList)  # Type
            self._write_identifier(parameterList)  # Name
            # More parameters?
            if self.tokenizer.symbol() == ",":
                self._write_symbol(parameterList)

    def compile_term(self, expression):
        term = ET.SubElement(expression, "term")
        match self.tokenizer.token_type():
            case "keyword":
                if self.tokenizer.keyword() in ["TRUE", "FALSE", "NULL", "THIS"]:
                    self._write_keyword(term)
            case "integerConstant":
                self._write_integer_constant(term)
            case "stringConstant":
                self._write_string_constant(term)
            case "identifier":
                self._write_identifier(term)

                # function call in let statement
                if self.tokenizer.token_matches_value("."):
                    self._write_symbol(term)  # .
                    self._write_identifier(term)  # identifier
                    self.compile_expression_list(term)

                # handling arrays
                if self.tokenizer.token_matches_value("["):
                    self._write_symbol(term)  # [
                    self.compile_expression(term)  # expression
                    self._write_symbol(term)  # ]

            # nested expressions
            case "symbol":
                if self.tokenizer.token_matches_value("("):
                    self._write_symbol(term)  # (
                    self.compile_expression(term)
                    self._write_symbol(term)  # )

                # if self.tokenizer.token_matches_value('-'):
                #    self._write_symbol(term)
                #    self.compile_term(term)

        if not term:
            expression.remove(term)

    def compile_expression(self, statement):
        expression = ET.SubElement(statement, "expression")
        # self.compile_term(expression)

        # handling unary operators
        if (
            self.tokenizer.token_matches_value("-")
            or self.tokenizer.token_matches_value("+")
            or self.tokenizer.token_matches_value("~")
        ):
            term = ET.SubElement(expression, "term")
            self._write_symbol(term)
            self.compile_term(term)
        else:
            self.compile_term(expression)

        while self.tokenizer.token_is_operator():

            self._write_symbol(expression)
            self.compile_term(expression)

    def compile_expression_list(self, root):
        self._write_symbol(root)  # '('

        expressionList = ET.SubElement(root, "expressionList")
        # While there are expressions...
        while not self.tokenizer.token_matches_value(")"):
            self.compile_expression(expressionList)
            if self.tokenizer.token_matches_value(","):
                self._write_symbol(expressionList)

        self._write_symbol(root)  # ')'

    def compile_let(self, statements):
        letStatement = ET.SubElement(statements, "letStatement")
        # "Let":
        self._write_keyword(letStatement)

        # Variable name:
        self._write_identifier(letStatement)

        if self.tokenizer.symbol() == "[":
            self._write_symbol(letStatement)  #'['
            self.compile_expression(letStatement)  # expr
            self._write_symbol(letStatement)  #']'

        self._write_symbol(letStatement)  # '='

        self.compile_expression(letStatement)
        self._write_symbol(letStatement)  #';'

    def compile_return(self, statements):
        returnStatement = ET.SubElement(statements, "returnStatement")
        # "Return"
        self._write_keyword(returnStatement)

        # if next token is not ; we need to return something
        if not self.tokenizer.token_matches_value(";"):
            self.compile_expression(returnStatement)

        # ;
        self._write_symbol(returnStatement)

    def compile_do(self, statements):
        doStatement = ET.SubElement(statements, "doStatement")
        # do
        self._write_keyword(doStatement)
        self._write_identifier(doStatement)  # Subroutine name/(class/var):

        if self.tokenizer.token_matches_value("."):
            self._write_symbol(doStatement)  # '.'
            self._write_identifier(doStatement)  # method name

        self.compile_expression_list(doStatement)

        # ;
        self._write_symbol(doStatement)

    def compile_if(self, statements):
        ifStatement = ET.SubElement(statements, "ifStatement")
        self._write_keyword(ifStatement)  # if
        self._write_symbol(ifStatement)  # (

        self.compile_expression(ifStatement)  # expressions
        self._write_symbol(ifStatement)  # )

        self._write_symbol(ifStatement)  # {
        self.compile_subroutine_statements(ifStatement)
        self._write_symbol(ifStatement)  # }
        if self.tokenizer.token_matches_value("else"):
            self._write_keyword(ifStatement)  # "Else"
            self._write_symbol(ifStatement)  # '{'
            self.compile_subroutine_statements(ifStatement)  # (...)
            self._write_symbol(ifStatement)  # '}'

    def compile_while(self, statements):
        whileStatement = ET.SubElement(statements, "whileStatement")
        self._write_keyword(whileStatement)  # if
        self._write_symbol(whileStatement)  # (

        self.compile_expression(whileStatement)  # expressions
        self._write_symbol(whileStatement)  # )

        self._write_symbol(whileStatement)  # {
        self.compile_subroutine_statements(whileStatement)
        self._write_symbol(whileStatement)  # }

    def compile_subroutine_statements(self, subroutineBody):
        statements = ET.SubElement(subroutineBody, "statements")
        # subroutine body can have differents kinds of statements:
        while not self.tokenizer.token_matches_value("}"):
            # let statements
            if self.tokenizer.keyword() == "LET":
                self.compile_let(statements)
            # return statements
            elif self.tokenizer.keyword() == "RETURN":
                self.compile_return(statements)
            # do statements
            elif self.tokenizer.keyword() == "DO":
                self.compile_do(statements)
            # if statements
            elif self.tokenizer.keyword() == "IF":
                self.compile_if(statements)
            # while statements
            elif self.tokenizer.keyword() == "WHILE":
                self.compile_while(statements)

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

        self._write_symbol(subroutineDec)  # ')'

        # function body can be comprised of variable declaration and statements
        # Body:
        subroutineBody = ET.SubElement(subroutineDec, "subroutineBody")
        self._write_symbol(subroutineBody)  # '{'

        # function variable definitions
        while self.tokenizer.keyword() == "VAR":
            self.compile_local_var_dec(subroutineBody)

        # function statements
        if not self.tokenizer.token_matches_value("}"):
            self.compile_subroutine_statements(subroutineBody)

        self._write_symbol(subroutineBody)  # '}' (end of subroutine body.)

    def compile_class(self):
        self._write_keyword(self.root)  # "Class"
        self._write_identifier(self.root)  #  className
        self._write_symbol(self.root)  # '{'

        # Variable declarations:
        while self.tokenizer.keyword() in ["STATIC", "FIELD"]:
            self.compile_class_var_dec()

        # Class' subroutines declarations:
        while self.tokenizer.token_text() in [
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

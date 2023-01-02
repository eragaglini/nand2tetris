import sys
import os
import ntpath
import xml.etree.cElementTree as ET
import pdb

try:
    import VMWriter
    import JackTokenizer
    import SymbolTable
    import utils
except ImportError:
    from . import VMWriter
    from . import JackTokenizer
    from . import SymbolTable
    from . import utils


class CompilationEngine:
    def __init__(self, inFilename=None, xml_output=False):
        if inFilename:
            vmFilename = os.path.splitext(inFilename)[0] + ".vm"
            self.vm_writer = VMWriter.VMWriter(vmFilename)
            self.symbol_table = SymbolTable.SymbolTable()
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

    def compile_var_dec(self):
        nLocals = 0
        keyword = self._get_keyword()  # field or static or var
        type = self._get_type()  # type of variable
        name = self._get_identifier()  # identifier of variable
        self._define_var(name, type, keyword)
        nLocals += 1

        # Are there more variables in the same line?
        while self.tokenizer.symbol() == ",":
            self._get_symbol()
            name = self._get_identifier()  # Var. name
            self._define_var(name, type, keyword)
            nLocals += 1

        self._get_symbol()  # ;
        return nLocals

    def compile_parameter_list(self):
        kind = "ARG"
        while not self.tokenizer.token_matches_value(")"):
            type = self._get_keyword()  # Type
            name = self._get_identifier()  # Name
            self._define_var(name, type, kind)
            # More parameters?
            if self.tokenizer.symbol() == ",":
                self._get_symbol()  # ,

    def compile_term(self):
        match self.tokenizer.token_type():
            case "keyword":
                if self.tokenizer.keyword() in ["TRUE", "FALSE", "NULL", "THIS"]:
                    kw = self._get_keyword()
                    if kw == "FALSE" or kw == "NULL":
                        self.vm_writer.write_push("constant", 0)
                    elif kw == "TRUE":
                        # -1 in two's complement.
                        self.vm_writer.write_push("constant", 0)
                        self.vm_writer.write_arithmetic("~")
                    elif kw == "THIS":
                        self.vm_writer.write_push("pointer", 0)

            case "integerConstant":
                self.vm_writer.write_push("constant", self._get_int_val())
            case "stringConstant":
                string_val = self.tokenizer.string_val()
                self.vm_writer.write_string(string_val)
            case "identifier":
                var_name = self._get_identifier()
                # if it's a variable, it should push its value
                # otherwise it won't do anything
                self._write_var_push(var_name)

                # Is it an array?
                if self.tokenizer.token_matches_value("["):  # '[' expression']'
                    self._get_symbol()  # '['
                    self.vm_writer.write_push(
                        "POINTER", 1
                    )  # Save the current THAT pointer
                    self.vm_writer.write_pop("TEMP", 0)  # into TEMP0.
                    # compile expression to get the index of the array
                    self.compile_expression()
                    # Adding the expression to the previously loaded base pointer:
                    self.vm_writer.write_arithmetic("+")
                    # pop resulting address to pointer 1
                    self.vm_writer.write_pop("POINTER", 1)
                    self.vm_writer.write_push("THAT", 0)  # Deferefencing into TEMP1.
                    self.vm_writer.write_pop("TEMP", 1)
                    # Re-establish THAT pointer.
                    self.vm_writer.write_push("TEMP", 0)
                    self.vm_writer.write_pop("POINTER", 1)

                    self.vm_writer.write_push("TEMP", 1)  # Push result.
                    self._get_symbol()  # ']'

                # Is it a subroutine call?
                elif self.tokenizer.token_matches_value("("):  # '(' expression ')'
                    self._write_subroutine_call(var_name)
                # Is it a method call?
                elif self.tokenizer.token_matches_value("."):
                    self._write_subroutine_call(var_name)

            # nested expressions
            case "symbol":
                if self.tokenizer.token_matches_value("("):
                    self._get_symbol()  # (
                    self.compile_expression()
                    self._get_symbol()  # )

    def compile_expression(self):
        # handling unary operators
        if self.tokenizer.token_matches_value(
            "-"
        ) or self.tokenizer.token_matches_value("~"):
            self._get_symbol()
            self.compile_term()
        else:
            self.compile_term()

        while self.tokenizer.token_is_operator():
            command = self._get_symbol()
            self.compile_term()
            self.vm_writer.write_arithmetic(command)

    def compile_expression_list(self):
        num = 0
        self._get_symbol()  # '('

        # While there are expressions...
        while not self.tokenizer.token_matches_value(")"):
            self.compile_expression()
            num += 1
            if self.tokenizer.token_matches_value(","):
                self._get_symbol()

        self._get_symbol()  # ')'
        return num

    def compile_let(self):
        # "Let":
        self._get_keyword()

        # Variable name:
        var_name = self._get_identifier()

        array = False
        if self.tokenizer.symbol() == "[":
            array = True
            self._write_var_push(var_name)
            self._get_symbol()  #'['
            self.compile_expression()  # expr
            self._get_symbol()  #']'
            self.vm_writer.write_arithmetic("+")
            self.vm_writer.write_pop("POINTER", 1)  # Push to the THAT pointer.

        self._get_symbol()  # '='
        self.compile_expression()

        if array:
            self.vm_writer.write_pop("THAT", 0)
        else:
            self._write_var_push(var_name)

        self._get_symbol()  #';'

    def compile_return(self):
        # "Return"
        self._get_keyword()

        # if next token is not ; we need to return something
        if not self.tokenizer.token_matches_value(";"):
            self.compile_expression()

        # ;
        self._get_symbol()

    def compile_do(self):
        self._get_keyword()
        subroutine_name = self._get_identifier()  # Subroutine name/(class/var)
        self._write_subroutine_call(subroutine_name)
        self._get_symbol()  # ;

    """
    def compile_if(self):
        self._write_keyword()  # if
        self._write_symbol()  # (

        self.compile_expression()  # expressions
        self._write_symbol()  # )

        self._write_symbol()  # {
        self.compile_subroutine_statements()
        self._write_symbol()  # }
        if self.tokenizer.token_matches_value("else"):
            self._write_keyword()  # "Else"
            self._write_symbol()  # '{'
            self.compile_subroutine_statements()  # (...)
            self._write_symbol()  # '}'

    def compile_while(self, statements):
        self._write_keyword(whileStatement)  # if
        self._write_symbol(whileStatement)  # (

        self.compile_expression(whileStatement)  # expressions
        self._write_symbol(whileStatement)  # )

        self._write_symbol(whileStatement)  # {
        self.compile_subroutine_statements(whileStatement)
        self._write_symbol(whileStatement)  # }
    """

    def compile_subroutine_statements(self):
        # subroutine body can have differents kinds of statements:
        while not self.tokenizer.token_matches_value("}"):
            # let statements
            if self.tokenizer.keyword() == "LET":
                self.compile_let()
            # return statements
            elif self.tokenizer.keyword() == "RETURN":
                self.compile_return()
            # do statements
            elif self.tokenizer.keyword() == "DO":
                self.compile_do()
            # if statements
            elif self.tokenizer.keyword() == "IF":
                self.compile_if()
            # while statements
            elif self.tokenizer.keyword() == "WHILE":
                self.compile_while()

    def compile_subroutine(self):
        # function signature
        self._get_keyword()  # constructor, method of function
        self._get_type()  # Return type
        subroutine_name = self._get_identifier()  # subroutine identifier
        self._get_symbol()  # '('

        # parameter list
        self.compile_parameter_list()

        self._get_symbol()  # ')'
        self._get_symbol()  # '{'

        nLocals = 0
        # function variable definitions
        while self.tokenizer.keyword() == "VAR":
            nLocals += self.compile_var_dec()

        # writing subroutine signature
        # declaring a function that has nLocals local variables
        self.vm_writer.write_function_signature(
            "{}.{}".format(self._class_name, subroutine_name), nLocals
        )

        # function body can be comprised of variable declaration and statements
        # Body:
        # function statements
        if not self.tokenizer.token_matches_value("}"):
            self.compile_subroutine_statements()

        self._get_symbol()  # '}' (end of subroutine body.)

    def compile_class(self):
        self._get_keyword()  # "Class"
        self._class_name = self._get_identifier()  #  className
        self._get_symbol()  # '{'

        # Variable declarations:
        while self.tokenizer.keyword() in ["STATIC", "FIELD"]:
            self.compile_var_dec()

        # Class' subroutines declarations:
        while self.tokenizer.token_text() in [
            "CONSTRUCTOR",
            "FUNCTION",
            "METHOD",
            "VOID",
        ]:
            self.compile_subroutine()
        self._get_symbol()  # '}'

    # --- PRIVATE functions --- #
    def _get_keyword(self):
        keyword = self.tokenizer.keyword()
        self.tokenizer.advance()
        return keyword

    def _get_identifier(self):
        identifier = self.tokenizer.identifier()
        self.tokenizer.advance()
        return identifier

    def _get_symbol(self):
        symbol = self.tokenizer.symbol()
        self.tokenizer.advance()
        return symbol

    def _get_int_val(self):
        int_val = self.tokenizer.int_val()
        self.tokenizer.advance()
        return int_val

    def _get_string_val(self):
        string_val = self.tokenizer.string_val()
        self.tokenizer.advance()
        return string_val

    def _get_type(self):
        if self.tokenizer.token_is_primitive_type():
            return self._get_keyword()
        else:
            return self._get_identifier()

    def _define_var(self, name, varType, kind):
        if not self.symbol_table.kind_of(name):
            self.symbol_table.define(name, varType, kind)

    def _write_var_push(self, var_name):
        """Writes the operations to push a variable depending on its kind."""
        var_kind = self.symbol_table.kind_of(var_name)
        if not var_kind:
            return

        var_index = self.symbol_table.index_of(var_name)
        if var_kind == "FIELD":
            self.vm_writer.write_push("THIS", var_index)
        elif var_kind == "STATIC":
            self.vm_writer.write_push("STATIC", var_index)
        elif var_kind == "LOCAL":
            self.vm_writer.write_push("LOCAL", var_index)
        elif var_kind == "ARG":
            self.vm_writer.write_push("ARGUMENT", var_index)

    def _write_subroutine_call(self, name, returns_void=False):
        call_name = ""
        method_name = ""
        push_pointer = False

        if self.tokenizer.token_matches_value("."):  # Method call.
            self._get_symbol()  # '.'
            method_name = self._get_identifier()

        if method_name == "":
            # Implicit class, equivalent to "self.method()".
            # Appending the current/local class name to the function,
            # and pushing the "this" pointer.
            push_pointer = True
            self.vm_writer.write_push("POINTER", 0)
            call_name = "%s.%s" % (self._class_name, name)
        else:
            kind = self.symbol_table.kind_of(name)
            if not kind:  # "name" is a class: call it directly.
                call_name = "%s.%s" % (name, method_name)
            else:
                t = self.symbol_table.type_of(name)  # Get the variable's class.
                call_name = "%s.%s" % (t, method_name)
                push_pointer = True  # Push the location to which the variable points.
                self._write_var_push(name)

        number_of_parameters = self.compile_expression_list()

        if push_pointer:
            number_of_parameters += 1

        self.vm_writer.write_call(call_name, number_of_parameters)

        if returns_void:  # Void functions return 0. We ignore that value.
            self.vm_writer.write_pop("TEMP", 0)


def main():
    if len(sys.argv) < 2:
        print("Error. Missing argument [filename]")
        return -1
    else:
        filename = sys.argv[1]

    comp_engine = CompilationEngine(filename)


if __name__ == "__main__":
    main()

import sys
import os

import VMWriter
import JackTokenizer
import SymbolTable


class CompilationEngine:
    def __init__(self, inFilename=None, xml_output=False):
        if inFilename:
            vmFilename = os.path.splitext(inFilename)[0] + ".vm"
            self.vm_writer = VMWriter.VMWriter(vmFilename)
            self.symbol_table = SymbolTable.SymbolTable()
            self.tokenizer = JackTokenizer.JackTokenizer(inFilename, xml_output)
            # Initializing context variables:
            self._label_index = 0
            self._if_index = 0
            self._while_index = 0
            self.compile_class()

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
                self.vm_writer.write_string(self._get_string_val())
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
                # unaryOp term
                if self._token_is_unary_operator():
                    # unaryOp term
                    symbol = self._get_symbol()
                    self.compile_term()
                    if symbol == "-":
                        symbol = "neg"
                    self.vm_writer.write_arithmetic(symbol)

    def compile_expression(self):
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

    def compile_if(self):
        self._if_index += 1

        self._get_keyword()  # "If"
        self._get_symbol()  # '('
        self.compile_expression()  # condition
        self._get_symbol()  # ')'
        self.vm_writer.write_arithmetic("~")

        false_label = "ifF%d" % self._if_index
        true_label = "ifT%d" % self._if_index
        end_if_label = "ifEnd%d" % self._if_index

        self.vm_writer.write_if(false_label)

        self._get_symbol()  # '{'
        self.vm_writer.write_label(true_label)
        self.compile_subroutine_statements()  # (...)
        self.vm_writer.write_goto(end_if_label)
        self._get_symbol()  # '}'

        self.vm_writer.write_label(false_label)
        if self.tokenizer.token_matches_value("else"):
            print("eccoci")
            self._get_keyword()  # "Else"
            self._get_symbol()  # '{'
            self.compile_subroutine_statements()  # (...)r
            self._get_symbol()  # '}'

        self.vm_writer.write_label(end_if_label)

    def compile_while(self):
        self._while_index += 1

        while_begin_label = "W%d" % self._while_index
        while_end_label = "Wend%d" % self._while_index

        self.vm_writer.write_label(while_begin_label)

        self._get_keyword()  # "While"
        self._get_symbol()  # '('
        self.compile_expression()  # condition
        self._get_symbol()  # ')'

        # While guard. Negating it and making a goto in case its false:
        self.vm_writer.write_arithmetic("~")
        self.vm_writer.write_if(while_end_label)

        self._get_symbol()  # '{'
        self.compile_subroutine_statements()
        self._get_symbol()  # '}'
        self.vm_writer.write_goto(while_begin_label)

        self.vm_writer.write_label(while_end_label)

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
        self.symbol_table.starts_subroutine()
        # function signature
        subroutine_type = self._get_keyword()  # constructor, method of function
        return_type = self._get_type()  # Return type
        subroutine_name = self._get_identifier()  # subroutine identifier

        if subroutine_type == "METHOD":
            self._define_var("this_ptr", "INT", "ARG")

        self._get_symbol()  # '('
        # parameter list
        self.compile_parameter_list()
        self._get_symbol()  # ')'
        self._get_symbol()  # '{'

        # subroutine body
        nLocals = 0
        # function variable definitions
        while self.tokenizer.keyword() == "VAR":
            nLocals += self.compile_var_dec()

        # writing subroutine signature
        # declaring a function that has nLocals local variables
        self.vm_writer.write_function_signature(
            "{}.{}".format(self._class_name, subroutine_name), nLocals
        )

        if subroutine_type == "METHOD":
            # Argument 0 of a constructor is the this pointer.
            # The first thing the function does is move it to the pointer register.
            self.vm_writer.write_push("ARGUMENT", 0)
            self.vm_writer.write_pop("POINTER", 0)

        elif subroutine_type == "CONSTRUCTOR":
            # If it is a method, invoke the OS functions to allocate space.
            self.vm_writer.write_alloc(self.symbol_table.var_count("FIELD"))
            # Then we set the this pointer to the assigned space.
            self.vm_writer.write_pop("POINTER", 0)

        # function body can be comprised of variable declaration and statements
        # function statements
        if not self.tokenizer.token_matches_value("}"):
            self.compile_subroutine_statements()

        self._get_symbol()  # '}' (end of subroutine body.)

        # End of subroutine body.
        # If the return type is void, we need to push some value.
        # That way the caller can always pop at least one value.
        if return_type == "VOID":
            self.vm_writer.write_push("constant", 0)

        self.vm_writer.write_return()

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

    def _token_is_unary_operator(self):
        return self.tokenizer.symbol() in ["-", "~"]


def main():
    if len(sys.argv) < 2:
        print("Error. Missing argument [filename]")
        return -1
    else:
        filename = sys.argv[1]

    comp_engine = CompilationEngine(filename)


if __name__ == "__main__":
    main()

class SymbolTable:
    def __init__(self) -> None:
        self._global = dict()
        self._local = dict()
        self._global_static_index = 0
        self._global_field_index = 0
        self._local_arg_index = 0
        self._local_var_index = 0

    def starts_subroutine(self):
        # The clear() method removes all items from the dictionary
        # everytime we have to compile a new subroutine, we need to reset
        # the local variable symbol table
        self._local.clear()
        self._local_arg_index = 0
        self._local_var_index = 0

    def define(name: str, type: str, kind: str):
        """
        adds a new variable to the symbol table with
        the given name, type and kind. Assigns to it the index value
        of that kind and adds 1 to the index

        Parameters
        ------------
            name: str
                name of the new variable
            type: str
                jack type (int, Point or other)
            kind: str
                STATIC, FIELD, ARG o VAR
        """
        pass

    def var_count(self, kind):
        """
        Args:
            kind (str): the kind of the variables of which we need to
            know the number (STATIC, FIELD, ARG o VAR)

        Returns:
            int: The number of variables of the given kind already defined in the current scope
        """
        kind = kind.upper()
        res = 0
        for (symbol, info) in self._local.items():
            if info[1] == kind:
                res += 1
        for (symbol, info) in self._global.items():
            if info[1] == kind:
                res += 1

        return res

    def type_of(self, name):
        """
        Returns:
            str: the type of the named identifier in the current scope
        """
        if name in self._local:
            return self._local[name][0]
        if name in self._global:
            return self._global[name][0]

    def kind_of(self, name):
        """
        Returns:
            str: the kind of the named identifier in the current scope
        """
        if name in self._local:
            return self._local[name][1]
        if name in self._global:
            return self._global[name][1]
        return "NONE"

    def index_of(self, name):
        """
        Returns:
            str: the index of the named identifier in the current scope
        """
        if name in self._local:
            return self._local[name][2]
        if name in self._global:
            return self._global[name][2]

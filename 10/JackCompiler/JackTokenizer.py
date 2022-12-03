import sys
import re
import ntpath
from dict2xml import dict2xml
import xml.etree.ElementTree as ET

import pdb

# String constants:
# TOKEN_TYPES = ["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"]

TOKEN_KEYWORDS = [
    "CLASS",
    "METHOD",
    "FUNCTION",
    "CONSTRUCTOR",
    "INT",
    "BOOLEAN",
    "CHAR",
    "VOID",
    "VAR",
    "STATIC",
    "FIELD",
    "LET",
    "DO",
    "IF",
    "ELSE",
    "WHILE",
    "RETURN",
    "TRUE",
    "FALSE",
    "NULL",
    "THIS",
]

SYMBOLS = [
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    ",",
    ";",
    "=",
    ".",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "~",
    "<",
    ">",
]

WHITE_SPACE = [" ", "\n", "\t"]


class JackTokenizer:
    def __init__(self, path) -> None:
        self.token_lst, self.token_dicts = self.get_token_lst_and_dict(path)

        xml_title = "tokens"
        xml_tag_pattern = re.compile(r"</?{}>".format(xml_title))
        inner_xml = re.sub(
            xml_tag_pattern,
            "",
            "".join(dict2xml(e, wrap="tokens") for e in self.token_dicts),
        )

        file_name = "{}T.xml".format(self.path_leaf(path).rsplit(".", 1)[0])
        with open(file_name, "w") as f:
            f.write("<{0}>{1}</{0}>".format(xml_title, inner_xml))

        with open(file_name) as xmlfile:
            lines = [line for line in xmlfile if line.strip() != ""]

        with open((file_name), "w") as xmlfile:
            xmlfile.writelines(lines)

        self._filename = file_name
        tree = ET.parse(self._filename)
        self._root = tree.getroot()
        self._cursor = 0

    def advance(self):
        self._cursor += 1

    def get_next_token(self):
        return self._root[self._cursor]

    def has_more_tokens(self):
        return self._cursor < len(self._root)

    def token_type(self):
        return self.get_next_token().tag

    def token_text(self):
        return self.get_next_token().text.strip().upper()

    def token_matches_value(self, value):
        return self.get_next_token().text.strip() == value

    def token_is_primitive_type(self):
        return self.get_next_token().text.upper().strip() in [
            "INT",
            "CHAR",
            "BOOLEAN",
            "VOID",
        ]

    def token_is_operator(self):
        return self.token_type() == "symbol" and self.symbol() in [
            "+",
            "-",
            "*",
            "/",
            "&",
            "|",
            "<",
            ">",
            "=",
        ]

    def check_and_return_value(self, token_type):
        if self.token_type() == token_type:
            if token_type != "stringConstant" and token_type != "identifier":
                return self.get_next_token().text.upper().strip()
            elif token_type == "identifier":
                return self.get_next_token().text.strip()
            else:
                return self.get_next_token().text
        else:
            raise ValueError(
                "Error, element '{}' with value: '{}' at line {} is not of type: {}. It's of type: {}".format(
                    self.token_type(),
                    self.get_next_token().text.strip(),
                    self._cursor + 2,
                    token_type,
                    self.token_type(),
                )
            )

    def symbol(self):
        return self.check_and_return_value("symbol")

    def keyword(self):
        return self.check_and_return_value("keyword")

    def intVal(self):
        return self.check_and_return_value("integerConstant")

    def stringVal(self):
        return self.check_and_return_value("stringConstant")

    def identifier(self):
        return self.check_and_return_value("identifier")

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    # removes all comments from input text
    def comment_remover(self, path):
        with open(path) as file:
            lines = []
            to_skip_line = False
            for line in file:
                line = line.strip()
                if not to_skip_line:
                    # single line comment
                    if line.startswith("//"):
                        continue
                    # starting a multi-line comment
                    if line.startswith("/*"):
                        if not line.endswith("*/"):
                            to_skip_line = True
                            continue
                        else:
                            continue
                    else:
                        if line != "":
                            lines.append(line.split("//")[0])
                else:
                    if line.endswith("*/"):
                        # closing a multi-line comment
                        to_skip_line = False
        return lines

    def word_dict(self, word_str):
        return {
            "keyword"
            if word_str.upper() in TOKEN_KEYWORDS
            # else "identifier": identifier
            else "identifier"
            if not word_str.isnumeric()
            else "integerConstant": word_str
        }

    def get_tokens(self, word):
        word_token_lst = []
        word_token_dict = []
        word_str = ""
        for el in word:
            if el not in SYMBOLS:
                word_str += el
            else:
                if len(word_str) >= 1:
                    word_token_lst.append(word_str)
                    word_token_dict.append(self.word_dict(word_str))
                    word_str = ""

                word_token_lst.append(el)
                word_token_dict.append({"symbol": " " + el + " "})
        if len(word_str) >= 1:
            word_token_lst.append(word_str)
            word_token_dict.append(self.word_dict(word_str))
            word_str = ""
        return word_token_lst, word_token_dict

    def split_words(self, line):
        # create list of words
        if '"' not in line:
            return line.split()
        else:
            # if there are string constants we need to split the line differently
            line = re.split(r"(plus|\"|\")", line)
            sep = '"'
            result = []
            for i in range(len(line)):
                if line[i] == '"':
                    continue
                elif line[i - 1] == '"':
                    if i + 1 in range(len(line)):
                        if line[i + 1] == '"':
                            result.append(sep + line[i] + sep)
                    else:
                        result += line[i].split()
                else:
                    result += line[i].split()
            return result

    def get_token_lst_and_dict(self, path):
        token_lst = []
        token_dicts = []
        # remove all comments
        lines = self.comment_remover(path)

        # reading each line
        for line in lines:
            # reading each word
            line = self.split_words(line)
            for word in line:
                if '"' in word:
                    token_lst.append(word)
                    token_dicts.append({"stringConstant": word[1:-1]})
                elif word.upper() in TOKEN_KEYWORDS:
                    token_lst.append(word)
                    # token_dicts.append({'keyword': word})
                    token_dicts.append({"keyword": " " + word + " "})
                # get every token contained in every element of list
                else:
                    word_token_lst, word_token_dict = self.get_tokens(word)
                    token_lst += word_token_lst
                    token_dicts += word_token_dict
        return token_lst, token_dicts


def main():
    if len(sys.argv) < 2:
        print("Error. Missing argument [filename]")
        return -1
    else:
        filename = sys.argv[1]

    jt = JackTokenizer(filename)


if __name__ == "__main__":
    main()

import re
from pathlib import Path
from typing import List

# String constants:
TOKEN_TYPES = ["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"]

TOKEN_KEYWORDS = ["CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", \
					"BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", \
					"LET", "DO", "IF", "ELSE", "WHILE", "RETURN", "TRUE", \
					"FALSE", "NULL", "THIS"]

SYMBOLS = ['(', ')', '[', ']', '{', '}', ',', ';', '=', '.', '+', '-', '*', \
		 '/', '&', '|', '~', '<', '>']

WHITE_SPACE = [' ', '\n', '\t']


class JackTokenizer():

    def __init__(self,path) -> None:
        self.tokens = self.initialize_tokenizer(path)

    # removes all comments from input text
    def comment_remover(self,text):
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, text).strip()

    
    def get_tokens(self,word) -> List:
        word_tokens = []
        identifier = ''
        if word in TOKEN_KEYWORDS:
            word_tokens.append(word)
        for el in word:
            if el not in SYMBOLS:
                identifier += el
            else:
                if len(identifier) >= 1:
                    word_tokens.append(identifier)
                    identifier = ''
                word_tokens.append(el)
        
        if len(identifier) >= 1:
            word_tokens.append(identifier)
        return word_tokens
        

    def initialize_tokenizer(self,path):
        with open(path) as file:
            tokens = []
            # reading each line
            for line in file:
                # reading each word
                for word in self.comment_remover(line).split():
                    if word.upper() in TOKEN_KEYWORDS:
                        tokens.append(word)
                    # get every token contained in every element of list
                    else:
                        tokens += self.get_tokens(word)
        return tokens
import re
import ntpath
from xml.dom.minidom import parseString
from dict2xml import dict2xml

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
        self.token_lst, self.token_dicts = self.get_token_lst_and_dict(path)
        
        xml_title = "tokens"
        xml_tag_pattern = re.compile(r'</?{}>'.format(xml_title))
        inner_xml = re.sub(xml_tag_pattern, '', ''.join(dict2xml(e, wrap ="tokens") for e in self.token_dicts))
        print('<{0}>{1}</{0}>'.format(xml_title, inner_xml))

        file_name = self.path_leaf(path).rsplit( ".", 1 )[ 0 ]
        with open('{}T.xml'.format(file_name), 'w') as f:
            file_name = self.path_leaf(path)
            f.write('<{0}>{1}</{0}>'.format(xml_title, inner_xml))
    
    def path_leaf(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

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

    
    def get_tokens(self,word):
        word_token_lst = []
        word_token_dict = []
        identifier = ''
        if word in TOKEN_KEYWORDS:
            word_token_lst.append(word)
            word_token_dict.append({'keyword': word})
        for el in word:
            if el not in SYMBOLS:
                identifier += el
            else:
                if len(identifier) >= 1:
                    word_token_lst.append(identifier)
                    word_token_dict.append({'identifier': identifier})
                    identifier = ''
                word_token_lst.append(el)
                word_token_dict.append({'symbol': el})
        
        if len(identifier) >= 1:
            word_token_lst.append(identifier)
            word_token_dict.append({'identifier': identifier})
        return word_token_lst,word_token_dict
        

    def get_token_lst_and_dict(self,path):
        with open(path) as file:
            token_lst = []
            token_dicts = []
            # reading each line
            for line in file:
                # reading each word
                for word in self.comment_remover(line).split():
                    if word.upper() in TOKEN_KEYWORDS:
                        token_lst.append(word)
                        token_dicts.append({'keyword': word})
                    # get every token contained in every element of list
                    else:
                        word_token_lst, word_token_dict = self.get_tokens(word)
                        token_lst += word_token_lst
                        token_dicts += word_token_dict
        return token_lst,token_dicts
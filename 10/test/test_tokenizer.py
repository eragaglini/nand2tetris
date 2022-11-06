# run with python3 -m pytest -v
import pytest
import os

from JackCompiler.JackTokenizer import JackTokenizer

tokenizer = JackTokenizer("/Users/edoardoragaglini/Desktop/nand2tetris/projects/10/ExpressionLessSquare/Main.jack")

def test_comment_remover():
    tokenizer = JackTokenizer("/Users/edoardoragaglini/Desktop/nand2tetris/projects/10/ExpressionLessSquare/Main.jack")
    assert tokenizer.comment_remover("let x = x + 1; // commento di prova test comment_remove\n") == "let x = x + 1;"    
    assert tokenizer.comment_remover("let x = x + 1; /* commento di prova test comment_remove */\n") == "let x = x + 1;"
    assert tokenizer.comment_remover("/* lungo commento \n di prova */") == ""

def test_initialize_tokenizer():
    assert tokenizer.tokens == [
        'class', 'Main', '{', \
            'static', 'boolean', 'test', ';', \
            'function', 'void', 'main', '(', ')', '{', \
                'var', 'SquareGame', 'game', ';', \
                'let', 'game', '=', 'game', ';', \
                'do', 'game', '.', 'run', '(', ')', ';', \
                'do', 'game', '.', 'dispose', '(', ')', ';', \
                'return', ';',  \
            '}', \
            'function', 'void', 'more', '(', ')', '{', \
                'var', 'boolean', 'b', ';', \
                'if', '(', 'b', ')', '{', \
                '}', \
                'else', '{', \
                '}', \
                'return', ';', \
            '}', \
        '}'
    ]
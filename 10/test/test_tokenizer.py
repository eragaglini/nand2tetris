# run with python3 -m pytest -v
import pytest

from JackCompiler.JackTokenizer import JackTokenizer


@pytest.fixture
def tokenizer():
    return JackTokenizer(
        "/Users/edoardoragaglini/Desktop/nand2tetris/projects/10/ExpressionLessSquare/Main.jack"
    )


def test_comment_remover(tokenizer):
    assert (
        tokenizer.comment_remover(
            "let x = x + 1; // commento di prova test comment_remove\n"
        )
        == "let x = x + 1;"
    )
    assert (
        tokenizer.comment_remover(
            "let x = x + 1; /* commento di prova test comment_remove */\n"
        )
        == "let x = x + 1;"
    )
    assert tokenizer.comment_remover("/* lungo commento \n di prova */") == ""

def test_split_line(tokenizer):
    assert tokenizer.split_words('let length = Keyboard.readInt("HOW MANY NUMBERS? ");') \
        == ['let', 'length', '=', 'Keyboard.readInt(', '"HOW MANY NUMBERS? "', ');']
    assert tokenizer.split_words('do Output.printInt(sum / length);') \
        == ['do', 'Output.printInt(sum', '/', 'length);']

def test_word_dict(tokenizer):
    assert tokenizer.word_dict('0') == {'integerConstant': '0'}
    assert tokenizer.word_dict('test_identifier') == {'identifier': 'test_identifier'}
    assert tokenizer.word_dict('class') == {'keyword': 'class'}

def test_get_token_lst_and_dict(tokenizer):
    assert tokenizer.token_lst == [
        "class",
        "Main",
        "{",
        "static",
        "boolean",
        "test",
        ";",
        "function",
        "void",
        "main",
        "(",
        ")",
        "{",
        "var",
        "SquareGame",
        "game",
        ";",
        "let",
        "game",
        "=",
        "game",
        ";",
        "do",
        "game",
        ".",
        "run",
        "(",
        ")",
        ";",
        "do",
        "game",
        ".",
        "dispose",
        "(",
        ")",
        ";",
        "return",
        ";",
        "}",
        "function",
        "void",
        "more",
        "(",
        ")",
        "{",
        "var",
        "boolean",
        "b",
        ";",
        "if",
        "(",
        "b",
        ")",
        "{",
        "}",
        "else",
        "{",
        "}",
        "return",
        ";",
        "}",
        "}",
    ]
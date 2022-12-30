# run with python3 -m pytest -v
import pytest

from JackCompiler import CompilationEngine


def test_symbol_table():
    compilation_engine = CompilationEngine.CompilationEngine(
        "Pong/Ball.jack",
    )
    assert compilation_engine.symbol_table._global == {
        "x": ("INT", "FIELD", 0),
        "y": ("INT", "FIELD", 1),
        "lengthx": ("INT", "FIELD", 2),
        "lengthy": ("INT", "FIELD", 3),
        "d": ("INT", "FIELD", 4),
        "straightD": ("INT", "FIELD", 5),
        "diagonalD": ("INT", "FIELD", 6),
        "invert": ("BOOLEAN", "FIELD", 7),
        "positivex": ("BOOLEAN", "FIELD", 8),
        "positivey": ("BOOLEAN", "FIELD", 9),
        "leftWall": ("INT", "FIELD", 10),
        "rightWall": ("INT", "FIELD", 11),
        "topWall": ("INT", "FIELD", 12),
        "bottomWall": ("INT", "FIELD", 13),
        "wall": ("INT", "FIELD", 14),
    }
    compilation_engine = CompilationEngine.CompilationEngine(
        "Pong/Bat.jack",
    )
    assert compilation_engine.symbol_table._global == {
        "x": ("INT", "FIELD", 0),
        "y": ("INT", "FIELD", 1),
        "width": ("INT", "FIELD", 2),
        "height": ("INT", "FIELD", 3),
        "direction": ("INT", "FIELD", 4),
    }
    compilation_engine = CompilationEngine.CompilationEngine(
        "Pong/PongGame.jack",
    )
    assert compilation_engine.symbol_table._global == {
        "instance": ("PongGame", "STATIC", 0),
        "bat": ("Bat", "FIELD", 0),
        "ball": ("Ball", "FIELD", 1),
        "wall": ("INT", "FIELD", 2),
        "exit": ("BOOLEAN", "FIELD", 3),
        "score": ("INT", "FIELD", 4),
        "lastWall": ("INT", "FIELD", 5),
        "batWidth": ("INT", "FIELD", 6),
    }

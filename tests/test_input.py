import pytest
from llm_compare.input import resolve_prompt

def test_prompt_required(monkeypatch):
    class In:
        def isatty(self): return True
    monkeypatch.setattr("sys.stdin", In())
    with pytest.raises(ValueError, match="prompt is required"):
        resolve_prompt(None)

def test_argument_prompt(monkeypatch):
    class In:
        def isatty(self): return True
    monkeypatch.setattr("sys.stdin", In())
    assert resolve_prompt("Hello") == "Hello"

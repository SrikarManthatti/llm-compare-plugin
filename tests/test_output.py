import json
import click
from click.testing import CliRunner
from llm_compare.compare import CompareResult
from llm_compare.output import display_json, result_lines


class Response:
    def text(self):
        return "hello"


def test_result_lines():
    assert result_lines(CompareResult("a", response=Response())) == [
        "Model: a",
        "--------",
        "hello",
    ]


def test_json_output():
    runner = CliRunner()

    @click.command()
    def command():
        display_json(
            [
                CompareResult("a", response=Response()),
                CompareResult("bad", error="boom"),
            ]
        )

    result = runner.invoke(command)

    assert result.exit_code == 0
    assert json.loads(result.output) == [
        {"model": "a", "response": "hello"},
        {"model": "bad", "error": "boom"},
    ]

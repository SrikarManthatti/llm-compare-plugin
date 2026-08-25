import click
from .compare import run_compare
from .input import resolve_prompt
from .output import display_json, display_one_by_one, display_side_by_side


def register_compare_command(cli):
    @click.command(name="compare")
    @click.argument("prompt", required=False)
    @click.option(
        "model_ids",
        "-m",
        "--model",
        multiple=True,
        help="Model to include in the comparison. Specify at least twice.",
    )
    @click.option("-s", "--system", help="System prompt to use for every model.")
    @click.option(
        "options",
        "-o",
        "--option",
        type=(str, str),
        multiple=True,
        help="Key/value options for the models.",
    )
    @click.option(
        "--json", "as_json", is_flag=True, help="Output comparison results as JSON."
    )
    def compare(prompt, model_ids, system, options, as_json):
        """
        Run the same prompt against multiple models and compare responses.
        """

        # 1. verify the models passed
        if len(model_ids) < 2:
            raise click.ClickException(
                "Compare requires at least two models. Specify them with -m/--model."
            )

        # 2. Resolving the prompts
        try:
            prompt = resolve_prompt(prompt)
        except ValueError as ve:
            raise click.ClickException(str(ve)) from ve

        # 3. Running the prompt against the models
        results = run_compare(
            prompt=prompt,
            model_ids=model_ids,
            system=system,
            options=dict(options),
        )

        if as_json:
            display_json(results)
        elif len(results) == 2:
            display_side_by_side(results)
        else:
            display_one_by_one(results)

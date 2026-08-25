import sys


def resolve_prompt(prompt):
    stdin_prompt = ""

    if not sys.stdin.isatty():
        stdin_prompt = sys.stdin.read()
    stdin_prompt = stdin_prompt.strip()

    if stdin_prompt and prompt:
        prompt = f"{stdin_prompt} {prompt}"
    elif stdin_prompt:
        prompt = stdin_prompt
    if not prompt:
        raise ValueError("A prompt is required for compare command")
    return prompt


def resolve_fragments(fragments, db=None):
    if not fragments:
        return []

    try:
        from llm.cli import resolve_fragments as core_resolve_fragments
    except ImportError as ie:
        raise ValueError(
            "Fragement resolution is not available with this LLM package version"
        )
    return core_resolve_fragments(db, fragments)

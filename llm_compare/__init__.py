"""
Init file register to register the compare command
"""

import llm

__version__ = "0.1.0"


@llm.hookimpl
def register_commands(cli):
    from .cli import register_compare_command

    register_compare_command(cli)

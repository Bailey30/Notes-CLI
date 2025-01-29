import argparse
from dataclasses import dataclass
from typing import Any


@dataclass
class Args:
    operation: str
    query: Any
    input: str


def getArgs() -> Args:
    """Gets and returns the command line arguements when the programme runs."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "operation",
        default="list",
        nargs="?",
        help="The action to perform. Either create, read, update, delete, list, mark-in-progress or mark-done.",
    )

    parser.add_argument(
        "query",
        default="",
        nargs="?",
        help="The ID or status of a note e.g. done, todo, in-progress",
    )

    parser.add_argument(
        "input",
        default="",
        nargs="?",
        help="The new or updated value of a note.",
    )

    args = parser.parse_args()

    if args.input == "" and args.operation == "create":
        args.input = args.query

    return Args(operation=args.operation, query=args.query, input=args.input)

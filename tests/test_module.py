from cli_notes.main import getArgs


def test_default_args():
    args = getArgs()

    assert args.operation == "list"
    assert args.query == ""
    assert args.input == ""


def test_custom_args():
    import sys

    sys.argv = ["main.py", "read", "1"]

    args = getArgs()

    assert args.operation == "read"
    assert args.query == "1"
    assert args.input == ""


def test_should_create_new_json_file_if_none_exists_and_add_note():


def test_should_add_note():


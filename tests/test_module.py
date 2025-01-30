import os
import sys
import pytest
import json

from cli_notes.args import Args
from cli_notes.main import get_args, main
from cli_notes.notes_repo import NotesRepository
from cli_notes.operations import (
    create_note,
    delete_note,
    filter_notes,
    get_note_by_id,
    update_note,
)
from cli_notes.utils.utils import Note

TEST_FILE_PATH = os.path.join(os.path.dirname(__file__), "../test_notes.json")


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    yield
    if os.path.isfile(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)


class TestArgs:
    def test_default_args(self):
        args = get_args()

        assert args.operation == "list"
        assert args.query == ""
        assert args.input == ""

    def test_custom_args(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["main.py", "read", "1"])

        args = get_args()

        assert args.operation == "read"
        assert args.query == "1"
        assert args.input == ""

    def test_invalid_args(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["main.py", "invalid", "1"])

        with pytest.raises(SystemExit):
            get_args()


class TestNotesRepository:
    def test_should_create_new_json_file_if_none_exists(self):
        file_before = os.path.isfile(TEST_FILE_PATH)
        repo = NotesRepository(file_path=TEST_FILE_PATH)

        repo.write_to_file([])

        file_after = os.path.isfile(TEST_FILE_PATH)

        assert file_before == False
        assert file_after == True

    def test_write_note_file(self):
        repo = NotesRepository(file_path=TEST_FILE_PATH)

        new_note = Note(id="0", contents="new note", status="in-progress")

        repo.write_to_file([new_note])

        assert len(repo.notes) == 1


class TestOperations:
    def test_should_create_note(self):
        repo = NotesRepository(TEST_FILE_PATH)
        args = Args(operation="create", query="contents", input="contents")
        new_note = create_note(args, repo)

        assert new_note.id == "0"
        assert new_note.contents == "contents"
        assert new_note.status == "todo"

    def test_should_update_note_if_exists(self):
        repo = NotesRepository(TEST_FILE_PATH)
        args = Args(operation="create", query="contents", input="contents")

        new_note = create_note(args, repo)
        repo.write_to_file([new_note])

        update_args = Args(
            operation="update", query="0", input="updated contents"
        )
        updated_note = update_note(
            repo, update_args, "updated contents", "contents"
        )

        assert updated_note is not None
        assert updated_note.contents == "updated contents"
        assert updated_note.id == "0"

    def test_should_warn_note_doesnt_exists_when_updating_one_that_doesnt(self):
        repo = NotesRepository(TEST_FILE_PATH)
        repo.write_to_file([])

        update_args = Args(
            operation="update", query="0", input="updated contents"
        )

        with pytest.raises(
            ValueError, match=f"Note with ID {update_args.query} not found."
        ):
            update_note(repo, update_args, "updated contents", "contents")

    def test_should_get_correct_note(self):
        repo = NotesRepository(TEST_FILE_PATH)
        note_one = Note(id="0", contents="one", status="todo")
        note_two = Note(id="1", contents="two", status="todo")
        repo.write_to_file([note_one, note_two])

        found_note_one = get_note_by_id(repo.notes, "0")
        found_note_two = get_note_by_id(repo.notes, "1")
        found_note_three = get_note_by_id(repo.notes, "2")

        assert found_note_one is not None
        assert found_note_two is not None
        assert found_note_three is None
        assert found_note_one.id == "0"
        assert found_note_two.id == "1"

    def test_should_delete_note(self):
        repo = NotesRepository(TEST_FILE_PATH)
        note = Note(id="0", contents="contents", status="todo")
        args = Args(operation="delete", query="0", input="")

        repo.write_to_file([note])

        assert len(repo.notes) == 1

        delete_note(repo, args)

        assert len(repo.notes) == 0

    def test_should_raise_error_when_deleting_nonexistant_note(self):
        repo = NotesRepository(TEST_FILE_PATH)
        repo.write_to_file([])
        args = Args(operation="delete", query="0", input="")

        with pytest.raises(
            ValueError, match=f"Note with ID {args.query} not found."
        ):
            delete_note(repo, args)

    def test_should_get_all_notes(self):
        repo = NotesRepository(TEST_FILE_PATH)
        note_one = Note(id="0", contents="one", status="todo")
        note_two = Note(id="1", contents="two", status="todo")
        repo.write_to_file([note_one, note_two])
        args = Args(operation="list", query="", input="")

        notes = filter_notes(repo)

        assert len(repo.notes) == 2

    def test_should_create_note_with_args(self, monkeypatch):
        file_path = TEST_FILE_PATH

        monkeypatch.setattr(sys, "argv", ["main.py", "create", "one"])

        monkeypatch.setenv("NOTES_FILE_PATH", TEST_FILE_PATH)

        main()

        with open(file_path, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["contents"] == "one"

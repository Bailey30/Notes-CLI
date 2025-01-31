from dataclasses import replace
from typing import List, Literal

from .args import Args

from cli_notes.utils.utils import find, Note
from cli_notes.notes_repo import NotesRepository


def create_note(args: Args, repo: NotesRepository) -> Note:
    """Creates a note and writes it to a json file."""

    existing_notes = repo.notes

    new_id = str(int(existing_notes[-1].id) + 1)

    new_note = Note(
        id=new_id,
        status="todo",
        contents=args.input,
    )

    existing_notes.append(new_note)

    repo.write_to_file(existing_notes)

    print("Created new note:")

    return new_note


def get_note_by_id(notes: List[Note], id: str) -> Note | None:
    note = find(lambda x: x.id == id, notes)

    if note is None:
        print(f"Note with id {id} does not exist.")
        return

    return note


def update_note(
    repo: NotesRepository,
    args: Args,
    new_value: str,
    key: Literal["contents", "status"] = "contents",
) -> Note | None:
    """Updates a note with the given id. Can updated either the status or the contents."""

    selected_note = get_note_by_id(repo.notes, args.query)

    if selected_note is None:
        raise ValueError(f"Note with ID {args.query} not found.")

    updated_note = replace(selected_note, **{key: new_value})

    updated_notes = [
        updated_note if note.id == args.query else note for note in repo.notes
    ]

    repo.write_to_file(updated_notes)

    print("Note updated:")

    return updated_note


def delete_note(repo: NotesRepository, args: Args) -> None:
    """Deletes not with given id and rewrites the json file."""

    selected_note = get_note_by_id(repo.notes, args.query)

    if selected_note is None:
        raise ValueError(f"Note with ID {args.query} not found.")

    notes_after_deletion = [
        note for note in repo.notes if note.id != args.query
    ]

    repo.write_to_file(notes_after_deletion)

    print(f"Note {args.query} deleted.")


def filter_notes(repo: NotesRepository, filter: str = "") -> List[Note]:
    """Prints notes to the console there match the filter critera. If criteria is given its prints all notes.."""

    filtered_notes = (
        repo.notes
        if filter == ""
        else [note for note in repo.notes if note.status == filter]
    )

    return filtered_notes


def print_notes(notes: List[Note]) -> None:
    for note in notes:
        print_note(note)


def print_note(note: Note | None) -> None:
    if note is None:
        return

    print("---------------")
    print(f"ID      : {note.id}")
    print(f"Status  : {note.status}")
    print(f"Contents: {note.contents}")

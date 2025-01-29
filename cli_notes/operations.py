import json
from dataclasses import asdict, replace
from typing import List, Literal

from .args import Args

from ..utils.utils import find, Note
from .notes_repo import NotesRepository


def create_note(args: Args, repo: NotesRepository) -> Note:
    """Creates a note and writes it to a json file."""

    existing_notes = repo.notes

    new_note = Note(
        id=str(len(existing_notes)), status="todo", contents=args.input
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
    newValue: str,
    key: Literal["contents", "status"] = "contents",
) -> Note | None:
    """Updates a note with the given id. Can updated either the status or the contents."""

    selected_note = get_note_by_id(repo.notes, args.query)

    if selected_note is None:
        print(f"Note with ID: {args.query} not found.")
        return

    updated_notes = [
        replace(note, **{key: newValue}) if note.id == args.query else note
        for note in repo.notes
    ]

    repo.write_to_file(updated_notes)

    print("Note updated:")

    updated_note = find(lambda x: x.id == args.query, updated_notes)

    return updated_note


def delete_note(repo: NotesRepository, args: Args) -> None:
    """Deletes not with given id and rewrites the json file."""

    notes_after_deletion = [
        note for note in repo.notes if note.id != args.query
    ]

    repo.write_to_file(notes_after_deletion)

    print(f"Note {args.query} deleted.")


def write_to_file(file_path: str, notes: List[Note]) -> None:
    """Writes notes to a json file."""

    with open(file_path, "w") as file:
        # Convert each Note dataclass into a dict so json.dump works
        json.dump([asdict(note) for note in notes], file, indent=2)


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

import os
from cli_notes.operations import (
    create_note,
    filter_notes,
    get_note_by_id,
    print_note,
    print_notes,
    update_note,
    delete_note,
)
from .args import get_args
from .notes_repo import NotesRepository


def main():
    args = get_args()

    # This file path gets set during tests to use a seperate testing json file.
    env_path = os.environ.get("NOTES_FILE_PATH")

    FILE_PATH = (
        env_path
        if env_path
        else os.path.join(os.path.dirname(__file__), "../notes.json")
    )

    repo = NotesRepository(file_path=FILE_PATH)

    match args.operation:
        case "new":
            print_note(create_note(args, repo))
        case "id":
            print_note(get_note_by_id(repo.notes, args.query))
        case "update":
            print_note(update_note(repo, args, args.input, "contents"))
        case "delete":
            print_note(delete_note(repo, args))
        case "list":
            print_notes(filter_notes(repo, args.query))
        case "mark-in-progress":
            print_note(update_note(repo, args, "in-progress", "status"))
        case "mark-done":
            print_note(update_note(repo, args, "done", "status"))


if __name__ == "__main__":
    main()

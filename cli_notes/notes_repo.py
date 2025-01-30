import json
from typing import List
from cli_notes.utils.utils import Note
from dataclasses import asdict


class NotesRepository:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self._notes: List[Note] = self._load_notes()

    def _load_notes(self) -> List[Note]:
        """
        Loads notes from a JSON file or returns an empty list
        if the file is empty or doesn't exist.
        """
        try:
            with open(self.file_path, "r") as file:
                content = file.read().strip()
                # File exists but is empty
                if not content:
                    return []

                # Parse the JSON into a list of dictionaries
                raw_notes = json.loads(content)

                # Convert the dictionaries into a list of Note dataclasses
                # ** is the argument unpacking operator
                return [Note(**note_dict) for note_dict in raw_notes]

        except FileNotFoundError:
            return []

    def write_to_file(self, updated_notes: List[Note]) -> None:
        """
        Write to a json file.
        """

        self._notes = updated_notes
        with open(self.file_path, "w") as file:
            # Convert each Note dataclass into a dict so json.dump works
            json.dump([asdict(note) for note in updated_notes], file, indent=2)

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value

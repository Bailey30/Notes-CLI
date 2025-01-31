from typing import TypeVar, Callable, List, Optional

from dataclasses import asdict, dataclass, replace

T = TypeVar("T")


@dataclass
class Note:
    id: str
    contents: str
    status: str


def find(condition: Callable[[T], bool], list: List[T]) -> Optional[T]:
    """Returns the found item in a list if it matches the condition, otherwise returns None"""

    return next((item for item in list if condition(item)), None)

import pickle
from pathlib import Path
from typing import Any


def pickle_object(obj: Any, path: Path) -> None:
    """Save a Python object to a pickle file, creating the parent folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)

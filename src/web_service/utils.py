import pickle
from pathlib import Path
from typing import Any


def load_object(path: Path) -> Any:
    """Load a Python object from a pickle file."""
    with open(path, "rb") as f:
        return pickle.load(f)

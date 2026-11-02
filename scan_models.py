from dataclasses import dataclass
from pathlib import Path

@dataclass
class CandidateImage:

    path: Path

    size_bytes: int

    width: int

    height: int

    requires_resize: bool

    severity: str = ""

    best_class: str = ""

    score: float = 0.0

@dataclass
class Detection:

    file_path: Path

    severity: str

    detection_class: str

    score: float
    
    file_name: str = ""

    width: int = 0

    height: int = 0
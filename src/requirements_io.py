from dataclasses import dataclass
from typing import List
import csv
from pathlib import Path

@dataclass
class Requirement:
    id: str
    text: str
    label: str  # "clear" or "ambiguous"

def load_requirements(path: Path) -> List[Requirement]:
    requirements: List[Requirement] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            requirements.append(
                Requirement(
                    id=row["id"],
                    text=row["text"],
                    label=row["label"].strip().lower()
                )
            )
    return requirements

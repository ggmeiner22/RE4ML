import re
from typing import List

def split_into_candidate_requirements(raw_text: str) -> List[str]:
    """
    Robust requirement extraction for TXT/PDF:
    - Supports numbered lists: 1., 2., 3.
    - Supports dash bullets: -, •, *
    - Uses natural requirement boundaries instead of periods only
    - Merges wrapped lines
    """
    lines = [ln.strip() for ln in raw_text.splitlines()]

    candidates: List[str] = []
    buffer: List[str] = []

    def flush():
        if not buffer:
            return
        full = " ".join(buffer).strip()
        # Strip leading numbering like "1.", "2)"
        full = re.sub(r"^\d+[\.\)]\s*", "", full)
        if len(full) > 10:  # shorter threshold to allow real reqs
            candidates.append(full)
        buffer.clear()

    numbered_req = re.compile(r"^\d+[\.\)]\s+")   # e.g. "1. " or "2) "
    bullet_req   = re.compile(r"^[-•*]\s+")
    
    for line in lines:
        if not line:
            flush()
            continue

        # If this line starts a NEW requirement (numbered or bullet)
        if numbered_req.match(line) or bullet_req.match(line):
            flush()
            buffer.append(line)
        else:
            # continuation line
            buffer.append(line)

    flush()
    return candidates

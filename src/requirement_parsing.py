from typing import List


def split_into_candidate_requirements(raw_text: str) -> List[str]:
    """
    Very simple heuristic:

    - Split on newlines
    - Strip whitespace
    - Filter out very short lines
    - Merge lines that were clearly wrapped paragraphs

    You can later replace this with better sentence/section parsing
    or detection of numbered requirements (REQ-1, 1.2.3, etc.).
    """
    lines = [ln.strip() for ln in raw_text.splitlines()]
    candidates: List[str] = []
    buffer: List[str] = []

    def flush_buffer():
        if buffer:
            joined = " ".join(buffer).strip()
            if len(joined) >= 20:  # ignore super-short fragments
                candidates.append(joined)
            buffer.clear()

    for ln in lines:
        if not ln:
            # blank line → end of a paragraph
            flush_buffer()
            continue

        # Accumulate lines into a paragraph; if line ends with a period,
        # we treat it as end of a requirement-like sentence.
        buffer.append(ln)
        if ln.endswith("."):
            flush_buffer()

    # flush at end
    flush_buffer()

    return candidates

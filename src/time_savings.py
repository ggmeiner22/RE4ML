"""
Utility classes for extracting time measurements from original requirements and
suggested rewrites, leveraging the average reading speed of a college-educated person.
"""

from dataclasses import dataclass
from typing import List


WORDS_READ_PER_MINUTE = 250


@dataclass
class Suggestion():
    """Internal class for capturing all relevant information for each suggested
    change.
    """
    original_requirement: str
    original_length: int
    original_reading_time: float
    suggested_rewrite: str
    suggested_length: int
    suggested_reading_time: float
    length_difference: int
    reading_time_difference: float  # minutes


class TimeSavings():
    """Calculate and track the potential time savings for a set of requirements.
    """

    def __init__(self):
        self._history: List[Suggestion] = []


    def get_total_rewrites_count(self) -> int:
        return len(self._history)
    

    def get_total_minutes_saved(self) -> float:
        total_minutes = sum(
            h.reading_time_difference
            for h in self._history
        )
        return total_minutes


    def get_time_savings(self, req: str, rewrite: str) -> int:
        """Get the number of minutes possibly saved by accepting the rewrite of the
        given requirement. A positive value is an improvement, zero is no change, and
        a negative value indicates that the original requirement is faster to read.
        """
        # Assumption: there is more than one word in each requirement
        req_len: int = len(req.split(' '))
        rewrite_len: int = len(rewrite.split(' '))
        len_diff = abs(req_len - rewrite_len)  # absolute value (size)

        req_read_time: float = req_len / WORDS_READ_PER_MINUTE
        rewrite_read_time: float = rewrite_len / WORDS_READ_PER_MINUTE
        # time diff may be <= zero
        time_diff = req_read_time - rewrite_read_time

        self._history.append(
            Suggestion(
                original_requirement=req,
                original_length=req_len,
                original_reading_time=req_read_time,
                suggested_rewrite=rewrite,
                suggested_length=rewrite_len,
                suggested_reading_time=rewrite_read_time,
                length_difference=len_diff,
                reading_time_difference=time_diff
            )
        )


    def print_summary(self) -> None:
        """Print a summary of the history.
        """
        print("=" * 80)
        print("\nTime Savings Summary:\n")
        print(f"{self.get_total_rewrites_count()} rewrites were suggested")
        print(
            f"""
{self.get_total_minutes_saved()} minutes 
of human reading time could be saved by accepting all suggested edits."""
        )

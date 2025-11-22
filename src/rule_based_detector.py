import re
from typing import Dict, Any, List
from .config import AMBIGUOUS_TERMS


class RuleBasedDetector:
    """
    Simple QuARS-style rule-based ambiguity detector.
    Output format:
        { "has_issue": bool, "reasons": [str] }
    """

    def __init__(self, ambiguous_terms=None):
        self.ambiguous_terms = ambiguous_terms or AMBIGUOUS_TERMS
        # precompile regexes
        self.term_patterns = [
            re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            for term in self.ambiguous_terms
        ]

    def analyze(self, text: str) -> Dict[str, Any]:
        reasons: List[str] = []

        # 1) look for ambiguous/vague terms
        for term, pat in zip(self.ambiguous_terms, self.term_patterns):
            if pat.search(text):
                reasons.append(f'Contains vague term "{term}"')

        # 2) heuristic: “minimize/maximize/optimize” without numeric target
        if re.search(r"\b(minimize|maximize|optimize)\b", text, re.IGNORECASE):
            if not re.search(r"\d", text):
                reasons.append("Optimization goal without numeric target")

        # 3) phrases like “as needed”, “where appropriate”
        if re.search(r"\bas needed\b|\bwhere appropriate\b", text, re.IGNORECASE):
            reasons.append("Condition depends on unstated criteria")

        has_issue = len(reasons) > 0
        return {"has_issue": has_issue, "reasons": reasons}

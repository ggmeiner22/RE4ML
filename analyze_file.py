#!/usr/bin/env python3
"""
Command-line tool to analyze a TXT or PDF file of requirements and
flag ambiguous / unclear ones using:

- A rule-based QuARS-style detector
- An optional LLM-based detector

Usage:
    python analyze_file.py path/to/file.pdf --detector both
"""

import argparse
from pathlib import Path
from typing import List

from src.rule_based_detector import RuleBasedDetector
from src.llm_detector import LLMDetector
from src.file_utils import load_text_from_txt, load_text_from_pdf
from src.requirement_parsing import split_into_candidate_requirements


def print_requirement_report(
    requirements: List[str],
    use_rule: bool,
    use_llm: bool,
):
    rb_detector = RuleBasedDetector() if use_rule else None
    llm_detector = LLMDetector() if use_llm else None

    for i, req in enumerate(requirements, start=1):
        print("=" * 80)
        print(f"[{i}] Requirement candidate:")
        print(req)
        print("-" * 80)

        if use_rule and rb_detector:
            rb_result = rb_detector.analyze(req)
            label = "ambiguous" if rb_result["has_issue"] else "clear"
            print(f"Rule-based verdict: {label.upper()}")
            if rb_result["reasons"]:
                for r in rb_result["reasons"]:
                    print(f"  • {r}")
            else:
                print("  • No issues detected by rule-based detector.")

        if use_llm and llm_detector:
            llm_result = llm_detector.analyze(req)
            llm_label = llm_result.get("label", "ambiguous").lower()
            reason = llm_result.get("reason", "")
            if llm_label not in ("clear", "ambiguous"):
                llm_label = "ambiguous"
            print(f"\nLLM-based verdict: {llm_label.upper()}")
            if reason:
                print(f"  • {reason}")
        print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a TXT or PDF file of requirements and flag ambiguous ones."
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the .txt or .pdf file to analyze",
    )
    parser.add_argument(
        "--detector",
        choices=["rule", "llm", "both"],
        default="both",
        help="Which detector to run (default: both)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    path = Path(args.file)

    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    ext = path.suffix.lower()
    if ext == ".txt":
        raw_text = load_text_from_txt(path)
    elif ext == ".pdf":
        raw_text = load_text_from_pdf(path)
    else:
        raise SystemExit("Unsupported file type. Use .txt or .pdf")

    print(f"Loaded file: {path}")
    print("Extracting candidate requirements...\n")

    candidates = split_into_candidate_requirements(raw_text)
    if not candidates:
        print("No candidate requirements found (after filtering).")
        return

    use_rule = args.detector in ("rule", "both")
    use_llm = args.detector in ("llm", "both")

    print_requirement_report(
        requirements=candidates,
        use_rule=use_rule,
        use_llm=use_llm,
    )


if __name__ == "__main__":
    main()

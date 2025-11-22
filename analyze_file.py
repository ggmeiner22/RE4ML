"""
Command-line tool to analyze a TXT file of requirements and
flag ambiguous / unclear ones using:

- A rule-based QuARS-style detector
- An optional LLM-based detector (with rewrite suggestions)

Usage:
    python analyze_file.py path/to/file.pdf --detector both --rewrite
"""

import argparse
from pathlib import Path
from typing import List
import sys
from io import StringIO
from datetime import datetime

from tqdm import tqdm

from src.rule_based_detector import RuleBasedDetector
from src.llm_detector import LLMDetector
from src.file_utils import load_text_from_txt, load_text_from_pdf
from src.requirement_parsing import split_into_candidate_requirements


def print_requirement_report(
    requirements: List[str],
    use_rule: bool,
    use_llm: bool,
    show_rewrite: bool,
):
    rb_detector = RuleBasedDetector() if use_rule else None
    llm_detector = LLMDetector() if use_llm else None

    # tqdm progress bar over requirements
    for i, req in enumerate(
        tqdm(requirements, desc="Analyzing requirements", unit="req"),
        start=1,
    ):
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
            rewrite = llm_result.get("rewrite", None)

            if llm_label not in ("clear", "ambiguous"):
                llm_label = "ambiguous"

            print(f"\nLLM-based verdict: {llm_label.upper()}")
            if reason:
                print(f"  • {reason}")

            if show_rewrite:
                if llm_label == "ambiguous" and rewrite:
                    print("\n  Suggested rewrite:")
                    print(f"    {rewrite}")
                elif llm_label == "clear":
                    print("\n  Suggested rewrite:")
                    print("    (requirement already clear; no rewrite needed)")
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
    parser.add_argument(
        "--rewrite",
        action="store_true",
        help="If set, and LLM detector is used, also show rewrite suggestions for clarity uplift.",
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

    # === NEW: set up results directory structure ===
    root_dir = Path("analyze_results")
    root_dir.mkdir(exist_ok=True)

    file_folder = root_dir / path.stem
    file_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = file_folder / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    log_path = run_dir / f"analysis_{path.stem}.txt"

    # === NEW: capture stdout so we can write everything to the log file ===
    console_capture = StringIO()
    real_stdout = sys.stdout
    sys.stdout = console_capture

    print(f"Loaded file: {path}")
    print("Extracting candidate requirements...\n")

    candidates = split_into_candidate_requirements(raw_text)
    if not candidates:
        print("No candidate requirements found (after filtering).")

        # Restore stdout and write log even in this case
        sys.stdout = real_stdout
        with log_path.open("w", encoding="utf-8") as f:
            f.write(console_capture.getvalue())

        print(f"No candidate requirements found. Full log saved to: {log_path}")
        print(f"Run directory: {run_dir}")
        return

    use_rule = args.detector in ("rule", "both")
    use_llm = args.detector in ("llm", "both")

    if args.rewrite and not use_llm:
        print("Note: --rewrite has no effect without LLM detector; enabling LLM automatically.")
        use_llm = True

    print_requirement_report(
        requirements=candidates,
        use_rule=use_rule,
        use_llm=use_llm,
        show_rewrite=args.rewrite,
    )

    # === Restore stdout and write captured log to file ===
    sys.stdout = real_stdout
    with log_path.open("w", encoding="utf-8") as f:
        f.write(console_capture.getvalue())

    print(f"Full analysis output saved to: {log_path}")
    print(f"Run directory: {run_dir}")


if __name__ == "__main__":
    main()

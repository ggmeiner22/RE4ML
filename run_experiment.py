from typing import List
from pathlib import Path
import argparse
import sys
from io import StringIO
from datetime import datetime
from tqdm import tqdm

from src.requirements_io import load_requirements, Requirement
from src.rule_based_detector import RuleBasedDetector
from src.llm_detector import LLMDetector
from src.evaluation import evaluate
from src.config import DATA_PATH


def run_rule_based(reqs: List[Requirement]) -> List[str]:
    rb = RuleBasedDetector()
    preds: List[str] = []
    for r in tqdm(reqs, desc="Rule-based detector", unit="req"):
        result = rb.analyze(r.text)
        preds.append("ambiguous" if result["has_issue"] else "clear")
    return preds


def run_llm_based(reqs: List[Requirement]) -> List[str]:
    llm = LLMDetector()
    preds: List[str] = []
    for r in tqdm(reqs, desc="LLM-based detector", unit="req"):
        result = llm.analyze(r.text)
        label = result.get("label", "ambiguous").lower()
        if label not in ("clear", "ambiguous"):
            label = "ambiguous"
        preds.append(label)
    return preds


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run RE4ML experiment on a labeled requirements CSV."
    )
    parser.add_argument(
        "csv",
        nargs="?",
        default=None,
        help="Path to the CSV file with labeled requirements."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    csv_path = Path(args.csv) if args.csv else DATA_PATH
    if not csv_path.exists():
        raise SystemExit(f"Labeled data file not found: {csv_path}")

    # === NEW: Directory setup ===
    root_dir = Path("experiment_results")
    root_dir.mkdir(exist_ok=True)

    csv_folder = root_dir / csv_path.stem
    csv_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = csv_folder / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # Capture console output
    console_capture = StringIO()
    real_stdout = sys.stdout
    sys.stdout = console_capture

    print(f"Running experiment on: {csv_path}\n")

    # Load requirements
    requirements = load_requirements(csv_path)

    # Rule-based evaluation
    rb_preds = run_rule_based(requirements)
    evaluate("Rule-Based Baseline (QuARS-style)", requirements, rb_preds)
    print("\n")

    # LLM-based evaluation
    llm_preds = run_llm_based(requirements)
    evaluate("LLM-Based Detector", requirements, llm_preds)
    print("\n")

    # TSV output
    out_tsv = run_dir / "results_comparison.tsv"
    with out_tsv.open("w", encoding="utf-8") as f:
        f.write("id\ttext\tgold\trule_based\tllm\n")
        for r, rb, llm in zip(requirements, rb_preds, llm_preds):
            f.write(f"{r.id}\t{r.text}\t{r.label}\t{rb}\t{llm}\n")

    print(f"Per-requirement comparison written to: {out_tsv}\n")

    # Restore stdout
    sys.stdout = real_stdout

    # Save log file
    log_filename = f"results_{csv_path.stem}.txt"
    log_path = run_dir / log_filename
    with log_path.open("w", encoding="utf-8") as f:
        f.write(console_capture.getvalue())

    print(f"Full experiment output saved to: {log_path}")
    print(f"TSV comparison saved to: {out_tsv}")
    print(f"Experiment run directory: {run_dir}")


if __name__ == "__main__":
    main()

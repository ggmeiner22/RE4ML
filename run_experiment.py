from typing import List
from pathlib import Path
import argparse

from src.requirements_io import load_requirements, Requirement
from src.rule_based_detector import RuleBasedDetector
from src.llm_detector import LLMDetector
from src.evaluation import evaluate
from src.config import DATA_PATH


def run_rule_based(reqs: List[Requirement]) -> List[str]:
    rb = RuleBasedDetector()
    preds: List[str] = []
    for r in reqs:
        result = rb.analyze(r.text)
        preds.append("ambiguous" if result["has_issue"] else "clear")
    return preds


def run_llm_based(reqs: List[Requirement]) -> List[str]:
    llm = LLMDetector()  # Ollama-based detector
    preds: List[str] = []
    for r in reqs:
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
        help="Path to the CSV file with labeled requirements (id,text,label). "
             "If omitted, uses the default in src/config.py."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Use passed CSV if provided, otherwise fallback to DATA_PATH
    csv_path = Path(args.csv) if args.csv else DATA_PATH

    if not csv_path.exists():
        raise SystemExit(f"Labeled data file not found: {csv_path}")

    print(f"Loading dataset: {csv_path}")
    requirements = load_requirements(csv_path)

    # Rule-based evaluation
    rb_preds = run_rule_based(requirements)
    evaluate("Rule-Based Baseline (QuARS-style)", requirements, rb_preds)

    # LLM-based evaluation
    llm_preds = run_llm_based(requirements)
    evaluate("LLM-based Detector", requirements, llm_preds)

    # Export detailed comparison
    out_path = Path("results_comparison.tsv")
    with out_path.open("w", encoding="utf-8") as f:
        f.write("id\ttext\tground-truth\trule_based\tllm\n")
        for r, rb, llm in zip(requirements, rb_preds, llm_preds):
            f.write(f"{r.id}\t{r.text}\t{r.label}\t{rb}\t{llm}\n")

    print(f"\nPer-requirement comparison written to: {out_path}")


if __name__ == "__main__":
    main()

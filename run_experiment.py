from typing import List
from pathlib import Path

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
    llm = LLMDetector(client=None)  # TODO: pass configured client
    preds: List[str] = []
    for r in reqs:
        result = llm.analyze(r.text)
        label = result.get("label", "ambiguous").lower()
        if label not in ("clear", "ambiguous"):
            label = "ambiguous"
        preds.append(label)
    return preds


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"Labeled data file not found: {DATA_PATH}")

    requirements = load_requirements(DATA_PATH)

    # Rule-based baseline
    rb_preds = run_rule_based(requirements)
    evaluate("Rule-Based Baseline (QuARS-style)", requirements, rb_preds)

    # LLM-based
    llm_preds = run_llm_based(requirements)
    evaluate("LLM-based Detector", requirements, llm_preds)

    # Optional: dump per-requirement comparison for expert review
    out_path = Path("results_comparison.tsv")
    with out_path.open("w", encoding="utf-8") as f:
        f.write("id\ttext\tgold\trule_based\tllm\n")
        for r, rb, llm in zip(requirements, rb_preds, llm_preds):
            f.write(f"{r.id}\t{r.text}\t{r.label}\t{rb}\t{llm}\n")

    print(f"\nPer-requirement comparison written to: {out_path}")


if __name__ == "__main__":
    main()

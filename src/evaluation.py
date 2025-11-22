from typing import List
from sklearn.metrics import precision_recall_fscore_support, classification_report
from .requirements_io import Requirement

LABEL_TO_INT = {"clear": 0, "ambiguous": 1}


def encode_labels(requirements: List[Requirement]) -> List[int]:
    return [LABEL_TO_INT[r.label] for r in requirements]


def encode_preds(labels: List[str]) -> List[int]:
    return [LABEL_TO_INT[l] for l in labels]


def evaluate(
    name: str,
    gold: List[Requirement],
    predicted_labels: List[str],
) -> None:
    y_true = encode_labels(gold)
    y_pred = encode_preds(predicted_labels)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", pos_label=1
    )

    print(f"=== {name} ===")
    print(f"Precision (ambiguous): {precision:.3f}")
    print(f"Recall    (ambiguous): {recall:.3f}")
    print(f"F1        (ambiguous): {f1:.3f}")
    print("\nDetailed report:")
    print(classification_report(y_true, y_pred, target_names=["clear", "ambiguous"]))

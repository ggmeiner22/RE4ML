from pathlib import Path

# Path to labeled dataset for experiments
DATA_PATH = Path("data/mixed_requirements.csv")

# Terms for QuARS-style rule-based ambiguity detection
AMBIGUOUS_TERMS = [
    "fast", "quick", "quickly", "user-friendly", "easy to use",
    "robust", "reliable", "efficient", "flexible", "scalable",
    "etc.", "as needed", "if possible", "when appropriate",
    "sufficient", "adequate", "optimize", "minimize", "maximize"
]

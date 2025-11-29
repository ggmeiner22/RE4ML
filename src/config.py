from pathlib import Path

# Path to labeled dataset for experiments
DATA_PATH = Path('data/mixed_requirements.csv')

# Terms for QuARS-style rule-based ambiguity detection
AMBIGUOUS_TERMS = [
    'adequate', 'as needed', 'better', 'could', 'easy to use', 'efficient', 'etc.',
    'fast', 'flexible', 'generally', 'if possible', 'it', 'maximize', 'many', 'may',
    'might', 'minimize', 'optimize', 'quick', 'quickly', 'reliable', 'robust',
    'scalable', 'several', 'significantly', 'should', 'some', 'sufficient', 'that',
    'these', 'this', 'user-friendly', 'usually', 'when appropriate', 'worse'
]

# Terms that are not ambiguous or do not improve accuracy
STOP_WORDS = [
    'a', 'an', 'and', 'by', 'for', 'in', 'into', 'no', 'of', 'on', 'the', 'to', 'with'
]

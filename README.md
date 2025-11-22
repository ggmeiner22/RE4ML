# RE4ML – Ambiguity Detector

This prototype:
- Trains/evaluates rule-based vs LLM-based ambiguity detection on a labeled requirements CSV.
- Provides a CLI `analyze_file.py` to scan a .txt or .pdf document and flag ambiguous requirements.

## Setup

```bash
pip install -r requirements.txt
```

## Run experiment on labeled CSV
```bash
python run_experiment.py
```

## Analyze a requirements document
```bash
python analyze_file.py path/to/file.pdf --detector both
```

Detectors:
- rule – only rule-based
- llm – only LLM-based
- both – compare both

## How to run with rewrites

### Rule-based + LLM, with rewrite suggestions
python analyze_file.py path/to/requirements.pdf --detector both --rewrite

### Only LLM with rewrites
python analyze_file.py path/to/requirements.txt --detector llm --rewrite

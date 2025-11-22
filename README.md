# RE4ML – Ambiguity Detector

This prototype:
- Trains/evaluates rule-based vs LLM-based ambiguity detection on a labeled requirements CSV.
- Provides a CLI `analyze_file.py` to scan a .txt or .pdf document and flag ambiguous requirements.

## Setup

```bash
python3 -m venv .venv
# Windows:
.\.venv\Scripts\Activate
# macOS/Linux:
source .venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

sudo snap install ollama
ollama pull llama3.1

ollama serve   # if not already running
```

## Analyze a requirements document
```bash
python3 analyze_file.py path/to/file.pdf --detector both
```

Detectors:
- rule – only rule-based
- llm – only LLM-based
- both – compare both

## How to run with rewrites

### Rule-based + LLM, with rewrite suggestions
```bash
python3 analyze_file.py data/sample_requirements.pdf --detector both --rewrite
```

### Only LLM with rewrites
```bash
python3 analyze_file.py path/to/requirements.txt --detector llm --rewrite
```

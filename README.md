# RE4ML – Ambiguity Detector

This prototype:
- Trains/evaluates rule-based vs LLM-based ambiguity detection on a labeled requirements CSV.
- Provides a CLI `analyze_file.py` to scan a .txt or .pdf document and flag ambiguous requirements.
- Provides an experiment `run_experiment.py` to show numerical data based on the requirements.

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

### How to run with rewrites

#### Rule-based + LLM, with rewrite suggestions
```bash
python3 analyze_file.py data/mixed_requirements.txt --detector both --rewrite
```

#### Only LLM with rewrites
```bash
python3 analyze_file.py data/mixed_requirements.txt --detector llm --rewrite
```
#### Args
| Flag              | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| `file`            | Path to `.txt` or `.pdf` file containing requirements        |
| `--detector rule` | Only run rule-based detector                                 |
| `--detector llm`  | Only run LLM-based detector (via Ollama)                     |
| `--detector both` | Run both (recommended)                                       |
| `--rewrite`       | Show improved rewrite suggestions for ambiguous requirements |

## Experimentation (Rule-Based vs LLM Evaluation)
The experiment compares:
- Ground-truth labels in data/requirements_labeled.csv
- Rule-based predictions
- LLM-based predictions (via Ollama)
- Outputs precision, recall, F1, and detailed reports

Run:
```bash
python run_experiment.py data/mixed_requirements.csv
```

This produces:
- Console metrics
- A TSV comparison file: `results_comparison.tsv`

### Metrics
| Term          | Meaning                                                                        |
| ------------- | ------------------------------------------------------------------------------ |
| **Support**   | Number of data points in the dataset that belong to that class (ground truth). |
| **Precision** | Of the predicted positives, how many were correct?                             |
| **Recall**    | Of the actual positives, how many were detected?                               |
| **F1**        | Harmonic mean of precision and recall.                                         |


# AI/ML Experiment & Evaluation Starter

A minimal, verifiable machine learning evaluation pipeline template demonstrating seed tracking, metric logging, and reproducible evaluation.

## Quick Start
```bash
# Run evaluation with explicit seed
python3 evaluate.py --seed 42

# Run tests
pytest tests/
```

## Verification Path
Run `python3 evaluate.py --seed 42` and verify it reports deterministic accuracy metrics without requiring large model weights.

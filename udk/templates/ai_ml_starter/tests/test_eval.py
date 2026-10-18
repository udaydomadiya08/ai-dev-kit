"""
Unit tests for AI/ML evaluation script.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root containing evaluate.py is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

try:
    from evaluate import compute_metrics
except ImportError:
    from udk.templates.ai_ml_starter.evaluate import compute_metrics


def test_compute_metrics_reproducibility():
    m1 = compute_metrics(seed=42, n_samples=50)
    m2 = compute_metrics(seed=42, n_samples=50)
    assert m1 == m2
    assert 0.0 <= m1["accuracy"] <= 1.0
    assert m1["samples"] == 50

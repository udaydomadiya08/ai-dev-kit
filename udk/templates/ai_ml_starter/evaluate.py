"""
Deterministic evaluation script for AI/ML starter template.
"""

from __future__ import annotations

import argparse
import random


def compute_metrics(seed: int, n_samples: int = 100) -> dict[str, float]:
    rng = random.Random(seed)
    # Generate deterministic synthetic predictions
    correct = sum(1 for _ in range(n_samples) if rng.random() > 0.2)
    accuracy = correct / n_samples
    loss = (1.0 - accuracy) * 0.5
    return {
        "accuracy": round(accuracy, 4),
        "loss": round(loss, 4),
        "samples": n_samples,
        "seed": seed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Evaluation Runner")
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--samples", type=int, default=100, help="Number of evaluation samples"
    )
    args = parser.parse_args()

    metrics = compute_metrics(args.seed, args.samples)
    print("--- Evaluation Results ---")
    print(f"Seed: {metrics['seed']}")
    print(f"Samples: {metrics['samples']}")
    print(f"Accuracy: {metrics['accuracy']}")
    print(f"Loss: {metrics['loss']}")
    return 0


if __name__ == "__main__":
    main()

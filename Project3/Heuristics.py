import os
import itertools
import subprocess
import json
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

# Define fixed weights for each heuristic as specified
weight_ranges = {
    "EMPTY_TILES_WEIGHT": [1],
    "MAX_TILE_WEIGHT": [75, 100, 125],
    "MONOTONICITY_WEIGHT": [7.5, 10, 12.5],
    "SMOOTHNESS_WEIGHT": [0.75, 1, 1.25],
    "MERGE_POTENTIAL_WEIGHT": [0.75, 1, 1.25],
    "WEIGHTED_TILE_WEIGHT": [100]
}

# Generate all combinations of weights
combinations = list(itertools.product(
    weight_ranges["EMPTY_TILES_WEIGHT"],
    weight_ranges["MAX_TILE_WEIGHT"],
    weight_ranges["MONOTONICITY_WEIGHT"],
    weight_ranges["SMOOTHNESS_WEIGHT"],
    weight_ranges["MERGE_POTENTIAL_WEIGHT"],
    weight_ranges["WEIGHTED_TILE_WEIGHT"]
))

REPEAT = 24

def run_game(weights):
    """Runs the 2048 game with the specified weights and returns all scores from five runs."""
    empty_weight, max_weight, mono_weight, smooth_weight, merge_weight, weighted_weight = weights

    # Set environment variables for this process
    os.environ["EMPTY_TILES_WEIGHT"] = str(empty_weight)
    os.environ["MAX_TILE_WEIGHT"] = str(max_weight)
    os.environ["MONOTONICITY_WEIGHT"] = str(mono_weight)
    os.environ["SMOOTHNESS_WEIGHT"] = str(smooth_weight)
    os.environ["MERGE_POTENTIAL_WEIGHT"] = str(merge_weight)
    os.environ["WEIGHTED_TILE_WEIGHT"] = str(weighted_weight)

    scores = []
    for _ in range(REPEAT):  # Repeat the game 5 times to gather all scores
        result = subprocess.run(["python3", "GameManager.py"], capture_output=True, text=True)
        try:
            score = int(result.stdout.strip().split()[-1])  # Adjust parsing if necessary
            scores.append(score)
        except (ValueError, IndexError):
            print("Error reading score from output:", result.stdout)

    avg_score = sum(scores) / len(scores) if scores else 0
    return {"weights": weights, "scores": scores, "average_score": avg_score}


if __name__ == "__main__":
    # Parallel execution of weight combinations
    results = []

    with ProcessPoolExecutor() as executor:
        # Submit all weight combinations for parallel processing
        futures = {executor.submit(run_game, weights): weights for weights in combinations}

        # Process completed tasks as they finish
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

        # Find the best result based on average score
    best_result = max(results, key=lambda x: x["average_score"])

    # Write all results to a JSON file
    output_file = "2048_heuristic_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    # Display the best result
    print("Best Weights:", best_result["weights"])
    print("Best Average Score:", best_result["average_score"])
    print(f"All results stored in {output_file}")
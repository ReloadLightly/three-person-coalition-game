"""M3c: three short 25-generation exploratory trajectories.

This is deliberately exploratory. It asks whether the reconstructed ecology remains
capable of evolutionary turnover across generations and whether the low-level
Reconstructed bookkeeping choices visibly dominate the dynamics. It does not test
the historical class/temporal-differentiation claims yet.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path
from random import Random

from three_person_coalition_game.evolution import (
    generation_step,
    historical_initial_population,
)


SEED_PAIRS = ((7, 11), (17, 23), (29, 31))
GENERATIONS = 25
ROUNDS = 1000
MUTATION_OUTCOMES = ("unchanged", "new", "merged", "blocked_at_cap")


def chromosome_record(chromosome):
    return {
        "initial_action": chromosome.initial_action,
        "genes": [list(gene) for gene in chromosome.leaves],
        "node_count": len(chromosome.nodes),
        "max_depth": max((len(node) for node in chromosome.nodes), default=0),
    }


def population_snapshot(generation, population, audit=None):
    frequencies = list(population.frequencies)
    snapshot = {
        "generation": generation,
        "species_count": len(population.chromosomes),
        "frequencies": frequencies,
        "dominant_frequency": max(frequencies),
        "frequency_entropy_nats": -sum(
            frequency * math.log(frequency)
            for frequency in frequencies
            if frequency > 0.0
        ),
        "mean_node_count": sum(
            len(chromosome.nodes)
            for chromosome in population.chromosomes
        )
        / len(population.chromosomes),
        "max_node_count": max(
            len(chromosome.nodes)
            for chromosome in population.chromosomes
        ),
        "max_memory_depth": max(
            max((len(node) for node in chromosome.nodes), default=0)
            for chromosome in population.chromosomes
        ),
    }

    if audit is not None:
        outcomes = Counter(event.outcome for event in audit.mutation_events)
        snapshot.update(
            {
                "mean_score": audit.mean_score,
                "score_min": min(audit.scores),
                "score_max": max(audit.scores),
                "extinct_count": len(audit.extinct),
                "mutation_outcomes": {
                    outcome: outcomes.get(outcome, 0)
                    for outcome in MUTATION_OUTCOMES
                },
            }
        )
    return snapshot


def run_trajectory(initial_seed: int, mutation_seed: int):
    population = historical_initial_population(Random(initial_seed))
    mutation_rng = Random(mutation_seed)
    payoff_cache = {}
    trajectory = [population_snapshot(0, population)]

    for generation in range(1, GENERATIONS + 1):
        audit = generation_step(
            population,
            mutation_rng,
            rounds=ROUNDS,
            payoff_cache=payoff_cache,
        )
        population = audit.after
        trajectory.append(population_snapshot(generation, population, audit))

    cap_generation = next(
        (
            row["generation"]
            for row in trajectory
            if row["species_count"] == 9
        ),
        None,
    )
    mutation_totals = {
        outcome: sum(
            row.get("mutation_outcomes", {}).get(outcome, 0)
            for row in trajectory[1:]
        )
        for outcome in MUTATION_OUTCOMES
    }

    return {
        "initial_seed": initial_seed,
        "mutation_seed": mutation_seed,
        "summary": {
            "species_cap_first_reached_generation": cap_generation,
            "total_extinctions": sum(
                row.get("extinct_count", 0)
                for row in trajectory[1:]
            ),
            "mutation_outcome_totals": mutation_totals,
            "final_mean_score": trajectory[-1]["mean_score"],
            "final_dominant_frequency": trajectory[-1]["dominant_frequency"],
            "final_max_memory_depth": trajectory[-1]["max_memory_depth"],
        },
        "trajectory": trajectory,
        "final_population": {
            "frequencies": list(population.frequencies),
            "chromosomes": [
                chromosome_record(chromosome)
                for chromosome in population.chromosomes
            ],
        },
        "unique_cached_matchups": len(payoff_cache),
    }


def diagnostic_row(run, snapshot):
    outcomes = snapshot.get("mutation_outcomes", {})
    return {
        "initial_seed": run["initial_seed"],
        "mutation_seed": run["mutation_seed"],
        "generation": snapshot["generation"],
        "species_count": snapshot["species_count"],
        "frequencies": " ".join(
            f"{value:.17g}" for value in snapshot["frequencies"]
        ),
        "dominant_frequency": snapshot["dominant_frequency"],
        "frequency_entropy_nats": snapshot["frequency_entropy_nats"],
        "mean_score": snapshot.get("mean_score", ""),
        "score_min": snapshot.get("score_min", ""),
        "score_max": snapshot.get("score_max", ""),
        "extinct_count": snapshot.get("extinct_count", ""),
        "mutation_unchanged": outcomes.get("unchanged", ""),
        "mutation_new": outcomes.get("new", ""),
        "mutation_merged": outcomes.get("merged", ""),
        "mutation_blocked_at_cap": outcomes.get("blocked_at_cap", ""),
        "mean_node_count": snapshot["mean_node_count"],
        "max_node_count": snapshot["max_node_count"],
        "max_memory_depth": snapshot["max_memory_depth"],
    }


def main() -> None:
    runs = [
        run_trajectory(initial_seed, mutation_seed)
        for initial_seed, mutation_seed in SEED_PAIRS
    ]
    configuration = {
        "generations": GENERATIONS,
        "seed_pairs": [list(pair) for pair in SEED_PAIRS],
        "rounds_per_seating": ROUNDS,
        "two_seatings_per_matchup": True,
        "initial_species": 6,
        "max_species": 9,
        "growth_constant": 0.2,
        "kill_limit": 0.2,
        "mutant_share": 0.1,
    }
    reconstructed_choices = {
        "initial_root_branch_probability": 0.5,
        "initial_action_probability": 0.5,
        "mutation_scheduler": "one_local_mutation_pass_per_surviving_species",
        "species_cap_rule": "block_novel_mutant_when_full",
        "multi_operator_order": [
            "PointAdd",
            "PointRemove",
            "Dupli",
            "RemoveRecursively",
        ],
    }

    evidence_dir = Path(__file__).resolve().parents[1] / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    summary_payload = {
        "artifact": "m3c_25_generation_exploration",
        "status": "exploratory",
        "claim_boundary": (
            "Three seeded 25-generation trajectories diagnose the reconstructed "
            "ecology and bookkeeping choices; they do not test historical regime replication."
        ),
        "configuration": configuration,
        "reconstructed_choices": reconstructed_choices,
        "runs": [
            {
                "initial_seed": run["initial_seed"],
                "mutation_seed": run["mutation_seed"],
                "summary": run["summary"],
                "final_population": run["final_population"],
                "unique_cached_matchups": run["unique_cached_matchups"],
            }
            for run in runs
        ],
    }
    (evidence_dir / "m3c_25_generation_summary.json").write_text(
        json.dumps(summary_payload, indent=2) + "\n",
        encoding="utf-8",
    )

    rows = [
        diagnostic_row(run, snapshot)
        for run in runs
        for snapshot in run["trajectory"]
    ]
    with (evidence_dir / "m3c_25_generation_diagnostics.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({"runs": [run["summary"] for run in runs]}, indent=2))


if __name__ == "__main__":
    main()

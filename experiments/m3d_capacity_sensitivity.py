"""M3d: bounded sensitivity to the species-capacity parameter.

M3c showed that the current nine-species cap is reached within 3--4 generations
and blocks most novel mutant proposals. The historical source explicitly sets the
maximum to 9, says a larger maximum should increase strategy variation, and says
the small value was chosen because three-person matchups become expensive.

The original full-cap bookkeeping is not preserved in the inspected sources.
M3d therefore does not invent a replacement rule. It keeps the current conservative
'block novel mutant when full' bookkeeping fixed and varies only capacity: 9, 12,
and 18. The historical value 9 remains the replication baseline; 12 and 18 are
explicit exploratory sensitivity variants.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from random import Random

from three_person_coalition_game.evolution import (
    generation_step,
    historical_initial_population,
)


SEED_PAIRS = ((7, 11), (17, 23), (29, 31))
MAX_SPECIES_VALUES = (9, 12, 18)
GENERATIONS = 25
ROUNDS = 1000
MUTATION_OUTCOMES = ("unchanged", "new", "merged", "blocked_at_cap")


def run_trajectory(max_species: int, initial_seed: int, mutation_seed: int):
    population = historical_initial_population(Random(initial_seed))
    mutation_rng = Random(mutation_seed)
    payoff_cache = {}
    rows = []
    cap_first_reached = None
    mutation_totals = Counter()
    total_extinctions = 0

    for generation in range(1, GENERATIONS + 1):
        audit = generation_step(
            population,
            mutation_rng,
            rounds=ROUNDS,
            max_species=max_species,
            payoff_cache=payoff_cache,
        )
        population = audit.after
        outcomes = Counter(event.outcome for event in audit.mutation_events)
        mutation_totals.update(outcomes)
        total_extinctions += len(audit.extinct)

        if cap_first_reached is None and len(population.chromosomes) == max_species:
            cap_first_reached = generation

        rows.append(
            {
                "max_species": max_species,
                "initial_seed": initial_seed,
                "mutation_seed": mutation_seed,
                "generation": generation,
                "species_count": len(population.chromosomes),
                "mean_score": audit.mean_score,
                "dominant_frequency": max(population.frequencies),
                "max_memory_depth": max(
                    max((len(node) for node in chromosome.nodes), default=0)
                    for chromosome in population.chromosomes
                ),
                "mutation_unchanged": outcomes.get("unchanged", 0),
                "mutation_new": outcomes.get("new", 0),
                "mutation_merged": outcomes.get("merged", 0),
                "mutation_blocked_at_cap": outcomes.get("blocked_at_cap", 0),
            }
        )

    return {
        "summary": {
            "max_species": max_species,
            "initial_seed": initial_seed,
            "mutation_seed": mutation_seed,
            "species_cap_first_reached_generation": cap_first_reached,
            "total_extinctions": total_extinctions,
            "mutation_outcome_totals": {
                outcome: mutation_totals.get(outcome, 0)
                for outcome in MUTATION_OUTCOMES
            },
            "final_mean_score": rows[-1]["mean_score"],
            "final_dominant_frequency": rows[-1]["dominant_frequency"],
            "final_max_memory_depth": rows[-1]["max_memory_depth"],
            "unique_cached_matchups": len(payoff_cache),
            "final_species_count": len(population.chromosomes),
        },
        "rows": rows,
    }


def main() -> None:
    runs = [
        run_trajectory(max_species, initial_seed, mutation_seed)
        for max_species in MAX_SPECIES_VALUES
        for initial_seed, mutation_seed in SEED_PAIRS
    ]

    evidence_dir = Path(__file__).resolve().parents[1] / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    payload = {
        "artifact": "m3d_capacity_sensitivity",
        "status": "exploratory_sensitivity",
        "claim_boundary": (
            "Matched starting seed pairs compare the historical maximum species "
            "value 9 with larger-cap variants 12 and 18 while keeping the same "
            "Reconstructed at-cap bookkeeping. This diagnoses capacity sensitivity; "
            "it does not recover the lost historical full-cap code or test the "
            "historical social-regime claims."
        ),
        "source_finding": (
            "Akiyama's 1995 Japanese exposition explicitly sets maximum species to "
            "9, states that larger maximum species should increase strategy variation, "
            "and explains that a larger value makes the three-person simulation much "
            "more expensive. The inspected source does not state what the program did "
            "when a novel mutant was proposed while every species slot was occupied."
        ),
        "configuration": {
            "generations": GENERATIONS,
            "seed_pairs": [list(pair) for pair in SEED_PAIRS],
            "rounds_per_seating": ROUNDS,
            "two_seatings_per_matchup": True,
            "max_species_values": list(MAX_SPECIES_VALUES),
            "growth_constant": 0.2,
            "kill_limit": 0.2,
            "mutant_share": 0.1,
        },
        "controlled_reconstructed_choices": {
            "initial_root_branch_probability": 0.5,
            "initial_action_probability": 0.5,
            "mutation_scheduler": "one_local_mutation_pass_per_surviving_species",
            "at_cap_behavior": "block_novel_mutant_when_full",
            "multi_operator_order": [
                "PointAdd",
                "PointRemove",
                "Dupli",
                "RemoveRecursively",
            ],
        },
        "runs": [run["summary"] for run in runs],
    }

    (evidence_dir / "m3d_capacity_sensitivity.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    rows = [row for run in runs for row in run["rows"]]
    with (evidence_dir / "m3d_capacity_sensitivity.csv").open(
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

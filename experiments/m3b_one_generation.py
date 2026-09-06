"""Run the first bounded M3b experiment: one generation, then stop."""

from __future__ import annotations

import json
from pathlib import Path
from random import Random

from three_person_coalition_game.evolution import (
    generation_step,
    historical_initial_population,
)

INITIAL_SEED = 7
MUTATION_SEED = 11
ROUNDS = 1000


def chromosome_record(chromosome):
    return {
        "initial_action": chromosome.initial_action,
        "genes": [list(gene) for gene in chromosome.leaves],
    }


def main() -> None:
    population = historical_initial_population(Random(INITIAL_SEED))
    audit = generation_step(
        population,
        Random(MUTATION_SEED),
        rounds=ROUNDS,
    )

    payload = {
        "artifact": "m3b_one_generation",
        "status": "implementation_validation",
        "claim_boundary": (
            "One source-anchored generation transition executes end-to-end; "
            "this is not evidence that the historical evolutionary regimes are reproduced."
        ),
        "configuration": {
            "initial_seed": INITIAL_SEED,
            "mutation_seed": MUTATION_SEED,
            "rounds_per_seating": ROUNDS,
            "two_seatings_per_matchup": True,
            "initial_species": 6,
            "initial_frequency_each": 1.0 / 6.0,
            "max_species": 9,
            "growth_constant": 0.2,
            "kill_limit": 0.2,
            "mutant_share": 0.1,
        },
        "reconstructed_choices": {
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
        },
        "before": {
            "frequencies": list(audit.before.frequencies),
            "chromosomes": [
                chromosome_record(chromosome)
                for chromosome in audit.before.chromosomes
            ],
        },
        "selection": {
            "scores": list(audit.scores),
            "mean_score": audit.mean_score,
            "fitness": list(audit.fitness),
            "extinct_indices": list(audit.extinct),
        },
        "mutation_events": [
            {
                "parent_index_after_extinction": event.parent_index,
                "outcome": event.outcome,
                "recipient_index": event.recipient_index,
                "mutant": chromosome_record(event.mutant),
            }
            for event in audit.mutation_events
        ],
        "after": {
            "species_count": len(audit.after.chromosomes),
            "frequencies": list(audit.after.frequencies),
            "chromosomes": [
                chromosome_record(chromosome)
                for chromosome in audit.after.chromosomes
            ],
        },
    }

    destination = Path(__file__).resolve().parents[1] / "evidence" / "m3b_one_generation.json"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

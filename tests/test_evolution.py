import unittest
from random import Random

from three_person_coalition_game.chromosome import Chromosome, MutationRates
from three_person_coalition_game.ecology import (
    historical_focal_payoff,
    selection_step,
)
from three_person_coalition_game.evolution import (
    HISTORICAL_INITIAL_SPECIES,
    PopulationState,
    generation_step,
    historical_initial_population,
)
from three_person_coalition_game.strategy import Strategy


class EvolutionTests(unittest.TestCase):
    def test_historical_matchup_averages_both_partner_seatings(self) -> None:
        focal = Strategy(0)
        left = Strategy.from_genes(0, [(0,), (1,), (2,), (3,), (4,)])
        right = Strategy.from_genes(0, [(0,), (1,), (2,), (3,), (5,)])

        # In one fixed orientation the focal averages 1.25 over 12 rounds; after
        # the source-required partner swap it averages 0.0. Historical evaluation
        # therefore uses both 12-round interactions: (1.25 + 0.0) / 2 = 0.625.
        self.assertAlmostEqual(
            historical_focal_payoff(focal, left, right, rounds=12),
            0.625,
        )
        self.assertAlmostEqual(
            historical_focal_payoff(focal, right, left, rounds=12),
            0.625,
        )

    def test_initial_population_has_six_distinct_equal_memory_one_species(self) -> None:
        population = historical_initial_population(Random(7))
        self.assertEqual(len(population.chromosomes), HISTORICAL_INITIAL_SPECIES)
        self.assertEqual(len(set(population.chromosomes)), HISTORICAL_INITIAL_SPECIES)
        self.assertTrue(
            all(abs(value - 1.0 / 6.0) < 1e-12 for value in population.frequencies)
        )
        self.assertTrue(
            all(
                all(len(node) == 1 for node in chromosome.nodes)
                for chromosome in population.chromosomes
            )
        )

    def test_selection_step_exposes_pre_normalization_population(self) -> None:
        step = selection_step(
            (0.5, 0.5),
            (3.0, 0.0),
            growth_constant=0.2,
            kill_limit=0.0,
        )
        self.assertAlmostEqual(step.frequencies[0], 0.65)
        self.assertAlmostEqual(step.frequencies[1], 0.35)

    def test_zero_mutation_generation_is_population_conserving(self) -> None:
        population = PopulationState(
            chromosomes=(
                Chromosome.from_genes(0, []),
                Chromosome.from_genes(1, [(state,) for state in range(8)]),
            ),
            frequencies=(0.5, 0.5),
        )
        audit = generation_step(
            population,
            Random(1),
            rounds=3,
            rates=MutationRates(0.0, 0.0, 0.0, 0.0),
            kill_limit=0.0,
        )
        self.assertAlmostEqual(sum(audit.after.frequencies), 1.0)
        self.assertEqual(len(audit.mutation_events), 2)
        self.assertTrue(
            all(event.outcome == "unchanged" for event in audit.mutation_events)
        )

    def test_mutant_receives_ten_percent_of_parent_population(self) -> None:
        parent = Chromosome.from_genes(0, [])
        population = PopulationState((parent,), (1.0,))
        audit = generation_step(
            population,
            Random(1),
            rounds=1,
            rates=MutationRates(
                point_add=1.0,
                point_remove=0.0,
                dupli=0.0,
                remove_recursively=0.0,
            ),
            kill_limit=0.0,
        )
        self.assertEqual(len(audit.after.chromosomes), 2)
        self.assertAlmostEqual(audit.after.frequencies[0], 0.9)
        self.assertAlmostEqual(audit.after.frequencies[1], 0.1)
        self.assertEqual(audit.mutation_events[0].outcome, "new")

    def test_reconstructed_species_cap_blocks_novel_mutant_without_mass_loss(self) -> None:
        parent = Chromosome.from_genes(0, [])
        population = PopulationState((parent,), (1.0,))
        audit = generation_step(
            population,
            Random(1),
            rounds=1,
            rates=MutationRates(1.0, 0.0, 0.0, 0.0),
            kill_limit=0.0,
            max_species=1,
        )
        self.assertEqual(audit.mutation_events[0].outcome, "blocked_at_cap")
        self.assertEqual(audit.after, population)


if __name__ == "__main__":
    unittest.main()

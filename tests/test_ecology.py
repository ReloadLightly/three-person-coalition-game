import unittest

from three_person_coalition_game.ecology import (
    HISTORICAL_GROWTH_CONSTANT,
    HISTORICAL_KILL_LIMIT,
    fitness_tensor,
    historical_focal_payoff,
    ordered_focal_payoff,
    species_scores,
    update_population,
)
from three_person_coalition_game.interaction import play_interaction
from three_person_coalition_game.strategy import Strategy


def always_zero() -> Strategy:
    return Strategy(0)


def always_one() -> Strategy:
    return Strategy.from_genes(1, [(state,) for state in range(8)])


class EcologyTests(unittest.TestCase):
    def test_ordered_focal_payoff_uses_focal_left_right_slots(self) -> None:
        zero = always_zero()
        one = always_one()
        self.assertEqual(ordered_focal_payoff(one, zero, zero, rounds=5), 0.0)
        self.assertEqual(ordered_focal_payoff(zero, one, zero, rounds=5), 3.0)
        self.assertEqual(ordered_focal_payoff(zero, zero, one, rounds=5), 3.0)

    def test_cycle_skipping_matches_explicit_two_seating_execution(self) -> None:
        focal = Strategy.from_genes(1, [(1, 2), (3, 5), (6,)])
        left = always_zero()
        right = always_one()
        rounds = 37
        first = play_interaction((focal, left, right), rounds=rounds)
        second = play_interaction((focal, right, left), rounds=rounds)
        explicit = (
            sum(record.payoffs[0] for record in first)
            + sum(record.payoffs[0] for record in second)
        ) / (2 * rounds)
        self.assertEqual(
            historical_focal_payoff(focal, left, right, rounds=rounds),
            explicit,
        )

    def test_fitness_tensor_contains_every_ordered_triple_including_self_play(self) -> None:
        strategies = (always_zero(), always_one())
        tensor = fitness_tensor(strategies, rounds=3)
        self.assertEqual(len(tensor), 8)
        self.assertIn((0, 0, 0), tensor)
        self.assertIn((0, 0, 1), tensor)
        self.assertIn((0, 1, 0), tensor)
        self.assertIn((1, 1, 1), tensor)

    def test_payoff_cache_reuses_deterministic_matchups(self) -> None:
        strategies = (always_zero(), always_one())
        cache = {}
        first = fitness_tensor(strategies, rounds=5, payoff_cache=cache)
        cached_count = len(cache)
        second = fitness_tensor(strategies, rounds=5, payoff_cache=cache)
        self.assertEqual(first, second)
        self.assertEqual(len(cache), cached_count)
        self.assertEqual(cached_count, 8)

    def test_species_scores_match_population_weighted_ordered_pairs(self) -> None:
        strategies = (always_zero(), always_one())
        frequencies = (0.75, 0.25)
        scores = species_scores(strategies, frequencies, rounds=4)
        expected = 3.0 * 2.0 * 0.75 * 0.25
        self.assertAlmostEqual(scores[0], expected)
        self.assertAlmostEqual(scores[1], expected)

    def test_equal_scores_leave_population_unchanged(self) -> None:
        update = update_population((0.7, 0.3), (1.5, 1.5))
        self.assertEqual(update.frequencies, (0.7, 0.3))
        self.assertEqual(update.fitness, (0.0, 0.0))
        self.assertEqual(update.extinct, ())

    def test_relative_fitness_growth_uses_historical_d(self) -> None:
        update = update_population(
            (0.5, 0.5),
            (3.0, 0.0),
            growth_constant=HISTORICAL_GROWTH_CONSTANT,
            kill_limit=0.0,
        )
        self.assertAlmostEqual(update.mean_score, 1.5)
        self.assertEqual(update.fitness, (1.5, -1.5))
        self.assertAlmostEqual(update.frequencies[0], 0.65)
        self.assertAlmostEqual(update.frequencies[1], 0.35)

    def test_below_average_species_below_kill_limit_goes_extinct(self) -> None:
        update = update_population(
            (0.5, 0.5),
            (3.0, 0.0),
            growth_constant=HISTORICAL_GROWTH_CONSTANT,
            kill_limit=0.4,
        )
        self.assertEqual(update.extinct, (1,))
        self.assertEqual(update.frequencies, (1.0, 0.0))

    def test_low_frequency_above_average_species_is_not_killed(self) -> None:
        update = update_population(
            (0.1, 0.9),
            (3.0, 0.0),
            growth_constant=0.0,
            kill_limit=HISTORICAL_KILL_LIMIT,
        )
        self.assertNotIn(0, update.extinct)
        self.assertEqual(update.frequencies, (0.1, 0.9))

    def test_invalid_population_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            species_scores((always_zero(),), (0.9,), rounds=2)
        with self.assertRaises(ValueError):
            update_population((0.5, 0.4), (1.0, 1.0))
        with self.assertRaises(ValueError):
            ordered_focal_payoff(always_zero(), always_zero(), always_zero(), rounds=0)


if __name__ == "__main__":
    unittest.main()

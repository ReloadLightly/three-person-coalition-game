import unittest

from three_person_coalition_game.ecology import (
    HISTORICAL_GROWTH_CONSTANT,
    HISTORICAL_KILL_LIMIT,
    fitness_tensor,
    ordered_focal_payoff,
    species_scores,
    update_population,
)
from three_person_coalition_game.strategy import Strategy


def always_zero() -> Strategy:
    return Strategy(0)


def always_one() -> Strategy:
    # Any non-empty history begins with exactly one state 0...7, so one of these
    # one-state genes always matches and card 1 is repeated forever.
    return Strategy.from_genes(1, [(state,) for state in range(8)])


class EcologyTests(unittest.TestCase):
    def test_ordered_focal_payoff_uses_focal_left_right_slots(self) -> None:
        zero = always_zero()
        one = always_one()
        self.assertEqual(ordered_focal_payoff(one, zero, zero, rounds=5), 0.0)
        self.assertEqual(ordered_focal_payoff(zero, one, zero, rounds=5), 3.0)
        self.assertEqual(ordered_focal_payoff(zero, zero, one, rounds=5), 3.0)

    def test_fitness_tensor_contains_every_ordered_triple_including_self_play(self) -> None:
        strategies = (always_zero(), always_one())
        tensor = fitness_tensor(strategies, rounds=3)
        self.assertEqual(len(tensor), 8)
        self.assertIn((0, 0, 0), tensor)
        self.assertIn((0, 0, 1), tensor)
        self.assertIn((0, 1, 0), tensor)
        self.assertIn((1, 1, 1), tensor)

    def test_species_scores_match_population_weighted_ordered_pairs(self) -> None:
        strategies = (always_zero(), always_one())
        frequencies = (0.75, 0.25)
        scores = species_scores(strategies, frequencies, rounds=4)

        # For either pure-card focal strategy, payoff 3 occurs exactly when one
        # partner shares its card and the other does not. Probability = 2pq.
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

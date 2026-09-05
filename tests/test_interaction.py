import unittest

from three_person_coalition_game.interaction import focal_states, play_interaction
from three_person_coalition_game.strategy import Strategy


class InteractionTests(unittest.TestCase):
    def test_source_action_sequence_reproduces_reported_focal_states(self) -> None:
        # Figure 3.2 / 18.2 reports these actions and state sequences.
        # White = 1 and black = 0 follows directly from the source state table.
        action_sequence = [
            (1, 0, 0),
            (0, 1, 1),
            (1, 1, 1),
            (1, 1, 1),
            (0, 1, 1),
            (0, 1, 0),
        ]
        expected_states = [
            (1, 2, 4),
            (6, 5, 3),
            (7, 7, 7),
            (7, 7, 7),
            (6, 5, 3),
            (4, 1, 2),
        ]

        observed = [tuple(state.index for state in focal_states(actions)) for actions in action_sequence]
        self.assertEqual(observed, expected_states)

    def test_three_constant_zero_strategies_remain_unanimous(self) -> None:
        strategies = [Strategy(0), Strategy(0), Strategy(0)]
        records = play_interaction(strategies, rounds=3)

        self.assertEqual(len(records), 3)
        for record in records:
            self.assertEqual(record.actions, (0, 0, 0))
            self.assertEqual(record.states, (0, 0, 0))
            self.assertEqual(record.payoffs, (0, 0, 0))

    def test_one_round_uses_each_strategy_initial_action(self) -> None:
        strategies = [Strategy(1), Strategy(0), Strategy(0)]
        record = play_interaction(strategies, rounds=1)[0]
        self.assertEqual(record.actions, (1, 0, 0))
        self.assertEqual(record.states, (1, 2, 4))
        self.assertEqual(record.payoffs, (0, 3, 3))

    def test_interaction_validates_shape_and_round_count(self) -> None:
        with self.assertRaises(ValueError):
            play_interaction([Strategy(0), Strategy(0)], rounds=1)
        with self.assertRaises(ValueError):
            play_interaction([Strategy(0), Strategy(0), Strategy(0)], rounds=-1)
        with self.assertRaises(ValueError):
            focal_states((0, 1))


if __name__ == "__main__":
    unittest.main()

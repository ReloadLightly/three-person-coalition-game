import unittest

from three_person_coalition_game.interaction import focal_states, play_interaction
from three_person_coalition_game.strategy import Strategy


class InteractionTests(unittest.TestCase):
    def test_source_round_orientation(self) -> None:
        # In the source example, player 3 has player 1 on the left and player 2
        # on the right. With actions (white, black, black) = (1, 0, 0), the
        # reported focal states are player1=1, player2=2, player3=4.
        states = tuple(state.index for state in focal_states((1, 0, 0)))
        self.assertEqual(states, (1, 2, 4))

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

import itertools
import unittest

from three_person_coalition_game import RoundState


class StageGameTests(unittest.TestCase):
    def test_all_eight_source_profiles(self) -> None:
        expected = {
            (0, 0, 0): (0, 0, 0),
            (0, 0, 1): (3, 3, 0),
            (0, 1, 0): (3, 0, 3),
            (0, 1, 1): (0, 3, 3),
            (1, 0, 0): (0, 3, 3),
            (1, 0, 1): (3, 0, 3),
            (1, 1, 0): (3, 3, 0),
            (1, 1, 1): (0, 0, 0),
        }

        for actions, payoffs in expected.items():
            with self.subTest(actions=actions):
                self.assertEqual(RoundState(*actions).payoffs, payoffs)

    def test_source_state_indexing(self) -> None:
        # Source example: (left, right, self) = (0, 1, 1) is state 3.
        self.assertEqual(RoundState(0, 1, 1).index, 3)
        # From the right player's perspective the same round is (1, 0, 1), state 5.
        self.assertEqual(RoundState(1, 0, 1).index, 5)

        for actions in itertools.product((0, 1), repeat=3):
            with self.subTest(actions=actions):
                state = RoundState(*actions)
                self.assertEqual(state.index % 2, state.self_)

    def test_binary_label_symmetry(self) -> None:
        for actions in itertools.product((0, 1), repeat=3):
            complement = tuple(1 - action for action in actions)
            with self.subTest(actions=actions):
                self.assertEqual(
                    RoundState(*actions).payoffs,
                    RoundState(*complement).payoffs,
                )

    def test_player_renaming_symmetry(self) -> None:
        for actions in itertools.product((0, 1), repeat=3):
            base_payoffs = RoundState(*actions).payoffs
            for permutation in itertools.permutations(range(3)):
                permuted_actions = tuple(actions[i] for i in permutation)
                permuted_payoffs = tuple(base_payoffs[i] for i in permutation)
                with self.subTest(actions=actions, permutation=permutation):
                    self.assertEqual(
                        RoundState(*permuted_actions).payoffs,
                        permuted_payoffs,
                    )

    def test_total_payoff(self) -> None:
        for actions in itertools.product((0, 1), repeat=3):
            state = RoundState(*actions)
            expected_total = 0 if len(set(actions)) == 1 else 6
            with self.subTest(actions=actions):
                self.assertEqual(sum(state.payoffs), expected_total)

    def test_rejects_nonbinary_actions(self) -> None:
        with self.assertRaises(ValueError):
            RoundState(0, 1, 2)


if __name__ == "__main__":
    unittest.main()

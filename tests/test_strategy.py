import unittest

from three_person_coalition_game.strategy import Strategy


class StrategyTests(unittest.TestCase):
    def test_initial_action_is_used_before_any_history_exists(self) -> None:
        self.assertEqual(Strategy.from_genes(1, [(6,)]).action([]), 1)
        self.assertEqual(Strategy.from_genes(0, [(6,)]).action([]), 0)

    def test_source_memory_one_example(self) -> None:
        strategy = Strategy.from_genes(0, [(6,)])
        self.assertEqual(strategy.action([6]), 1)
        self.assertEqual(strategy.action([1]), 0)

    def test_source_prefix_matching_example(self) -> None:
        # Source example: B = 3546 and gene A = 35 -> play white/card 1.
        # The public API accepts chronological history, hence [6, 4, 5, 3].
        strategy = Strategy.from_genes(0, [(3, 5)])
        self.assertEqual(strategy.action([6, 4, 5, 3]), 1)

    def test_short_transient_history_can_match_longer_gene(self) -> None:
        # The 8-ary coding explicitly defines decisions before full memory is available.
        strategy = Strategy.from_genes(0, [(3, 5, 4, 6)])
        self.assertEqual(strategy.action([5, 3]), 1)

    def test_nonmatching_history_plays_card_zero(self) -> None:
        strategy = Strategy.from_genes(1, [(3, 5), (1, 2)])
        self.assertEqual(strategy.action([7, 7, 7]), 0)

    def test_overlapping_genes_keep_the_longer_path(self) -> None:
        strategy = Strategy.from_genes(0, [(1, 2), (1, 2, 3), (4, 3)])
        self.assertEqual(strategy.genes, ((1, 2, 3), (4, 3)))
        self.assertEqual(strategy.memory_length, 3)

    def test_source_figure_gene_set_is_representable(self) -> None:
        strategy = Strategy.from_genes(0, [(1, 2), (1, 5, 0), (1, 5, 7), (4, 3)])
        self.assertEqual(strategy.memory_length, 3)
        self.assertEqual(
            strategy.genes,
            ((1, 2), (1, 5, 0), (1, 5, 7), (4, 3)),
        )

    def test_invalid_values_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Strategy.from_genes(2, [(1,)])
        with self.assertRaises(ValueError):
            Strategy.from_genes(0, [(8,)])
        with self.assertRaises(ValueError):
            Strategy.from_genes(0, [()])
        with self.assertRaises(ValueError):
            Strategy.from_genes(0, [(1,)]).action([9])


if __name__ == "__main__":
    unittest.main()

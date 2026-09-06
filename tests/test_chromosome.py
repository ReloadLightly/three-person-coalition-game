import itertools
import random
import unittest

from three_person_coalition_game.chromosome import (
    RECONSTRUCTED_MUTATION_ORDER,
    Chromosome,
    MutationRates,
)


class ChromosomeTests(unittest.TestCase):
    def test_source_gene_paths_build_a_prefix_closed_tree(self) -> None:
        chromosome = Chromosome.from_genes(
            0,
            [(1, 2), (1, 5, 0), (1, 5, 7), (4, 3)],
        )
        self.assertEqual(
            chromosome.leaves,
            ((1, 2), (1, 5, 0), (1, 5, 7), (4, 3)),
        )
        self.assertIn((1,), chromosome.nodes)
        self.assertIn((1, 5), chromosome.nodes)
        self.assertIn((4,), chromosome.nodes)

    def test_point_add_adds_one_absent_branch(self) -> None:
        chromosome = Chromosome.from_genes(0, [(1, 2)])
        mutated = chromosome.point_add((1, 3))
        self.assertIn((1, 3), mutated.nodes)
        self.assertEqual(mutated.leaves, ((1, 2), (1, 3)))

    def test_point_remove_removes_terminal_branch_only(self) -> None:
        chromosome = Chromosome.from_genes(0, [(1, 2), (1, 3)])
        mutated = chromosome.point_remove((1, 2))
        self.assertNotIn((1, 2), mutated.nodes)
        self.assertIn((1,), mutated.nodes)
        self.assertEqual(mutated.leaves, ((1, 3),))
        with self.assertRaises(ValueError):
            chromosome.point_remove((1,))

    def test_dupli_attaches_all_eight_children(self) -> None:
        chromosome = Chromosome.from_genes(0, [(3, 5)])
        duplicated = chromosome.dupli((3, 5))
        self.assertEqual(
            duplicated.children((3, 5)),
            tuple((3, 5, state) for state in range(8)),
        )

    def test_dupli_is_behaviorally_neutral(self) -> None:
        chromosome = Chromosome.from_genes(0, [(3, 5)])
        duplicated = chromosome.dupli((3, 5))
        before = chromosome.to_strategy()
        after = duplicated.to_strategy()

        for length in range(1, 5):
            for history in itertools.product(range(8), repeat=length):
                with self.subTest(history=history):
                    self.assertEqual(before.action(history), after.action(history))

    def test_remove_recursively_deletes_complete_subtree(self) -> None:
        chromosome = Chromosome.from_genes(
            0,
            [(1, 2), (1, 5, 0), (1, 5, 7), (4, 3)],
        )
        mutated = chromosome.remove_recursively((1, 5))
        self.assertNotIn((1, 5), mutated.nodes)
        self.assertNotIn((1, 5, 0), mutated.nodes)
        self.assertNotIn((1, 5, 7), mutated.nodes)
        self.assertEqual(mutated.leaves, ((1, 2), (4, 3)))

    def test_historical_rates_and_reconstructed_order_are_explicit(self) -> None:
        self.assertEqual(MutationRates(), MutationRates(0.1, 0.1, 0.001, 0.001))
        self.assertEqual(
            RECONSTRUCTED_MUTATION_ORDER,
            ("PointAdd", "PointRemove", "Dupli", "RemoveRecursively"),
        )

    def test_zero_rate_mutation_is_identity(self) -> None:
        chromosome = Chromosome.from_genes(1, [(1, 2), (4, 3)])
        mutated = chromosome.mutate(
            random.Random(7),
            MutationRates(0.0, 0.0, 0.0, 0.0),
        )
        self.assertEqual(mutated, chromosome)

    def test_invalid_tree_depth_and_non_prefix_closed_nodes_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Chromosome.from_genes(0, [(1, 2, 3, 4, 5)])
        with self.assertRaises(ValueError):
            Chromosome(0, frozenset({(1, 2)}))


if __name__ == "__main__":
    unittest.main()

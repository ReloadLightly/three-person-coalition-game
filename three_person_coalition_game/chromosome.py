"""Explicit 8-ary chromosome and historical mutation operators.

M2 could represent a strategy by its maximal gene paths because only action choice
mattered. M3 needs branch topology. This module therefore stores the prefix-closed
set of non-root nodes in the historical 8-ary tree while preserving conversion to
the M2 action semantics.

The four source mechanisms are PointAdd, PointRemove, Dupli, and
RemoveRecursively. Their causal actions and baseline rates are source-recovered.
Candidate-slot enumeration and the multi-operator order are reconstructed low-level
implementation details and are deliberately explicit here.
"""

from dataclasses import dataclass
from random import Random
from typing import Iterable, Sequence

from .game import Action
from .strategy import Gene, Strategy


HISTORICAL_MAX_MEMORY = 4
RECONSTRUCTED_MUTATION_ORDER = (
    "PointAdd",
    "PointRemove",
    "Dupli",
    "RemoveRecursively",
)


def _is_prefix(prefix: Sequence[int], sequence: Sequence[int]) -> bool:
    return len(prefix) <= len(sequence) and tuple(sequence[: len(prefix)]) == tuple(prefix)


@dataclass(frozen=True)
class MutationRates:
    """Historical baseline local mutation rates from the detailed sources."""

    point_add: float = 0.1
    point_remove: float = 0.1
    dupli: float = 0.001
    remove_recursively: float = 0.001

    def __post_init__(self) -> None:
        for value in (
            self.point_add,
            self.point_remove,
            self.dupli,
            self.remove_recursively,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("mutation rates must lie in [0, 1]")


@dataclass(frozen=True)
class Chromosome:
    """Prefix-closed explicit 8-ary strategy chromosome.

    ``nodes`` contains every non-root node that currently exists in the tree. Each
    node is represented by the state sequence from the root to that node. The root
    itself is implicit as ``()``.
    """

    initial_action: Action
    nodes: frozenset[Gene] = frozenset()
    max_memory: int = HISTORICAL_MAX_MEMORY

    def __post_init__(self) -> None:
        if self.initial_action not in (0, 1):
            raise ValueError("initial_action must be 0 or 1")
        if self.max_memory < 1:
            raise ValueError("max_memory must be positive")

        for node in self.nodes:
            if not node:
                raise ValueError("the root is implicit and must not appear in nodes")
            if len(node) > self.max_memory:
                raise ValueError("node depth exceeds max_memory")
            if any(state not in range(8) for state in node):
                raise ValueError("tree states must be integers from 0 through 7")
            for depth in range(1, len(node)):
                if node[:depth] not in self.nodes:
                    raise ValueError("nodes must form a prefix-closed tree")

    @classmethod
    def from_genes(
        cls,
        initial_action: Action,
        genes: Iterable[Sequence[int]],
        max_memory: int = HISTORICAL_MAX_MEMORY,
    ) -> "Chromosome":
        """Build the explicit tree from source-style maximal gene paths."""

        nodes: set[Gene] = set()
        for raw_gene in genes:
            gene = tuple(raw_gene)
            if not gene:
                raise ValueError("genes must contain at least one state")
            if len(gene) > max_memory:
                raise ValueError("gene depth exceeds max_memory")
            if any(state not in range(8) for state in gene):
                raise ValueError("gene states must be integers from 0 through 7")
            for depth in range(1, len(gene) + 1):
                nodes.add(gene[:depth])
        return cls(initial_action=initial_action, nodes=frozenset(nodes), max_memory=max_memory)

    def children(self, node: Sequence[int] = ()) -> tuple[Gene, ...]:
        """Return the existing direct children of ``node``."""

        parent = tuple(node)
        if parent and parent not in self.nodes:
            raise ValueError("node is not present in the chromosome")
        return tuple(
            sorted(
                candidate
                for candidate in self.nodes
                if len(candidate) == len(parent) + 1 and candidate[:-1] == parent
            )
        )

    @property
    def leaves(self) -> tuple[Gene, ...]:
        """Return maximal genes / terminal nodes."""

        return tuple(sorted(node for node in self.nodes if not self.children(node)))

    def to_strategy(self) -> Strategy:
        """Return the action-equivalent M2 finite-history strategy."""

        return Strategy.from_genes(self.initial_action, self.leaves)

    @property
    def point_add_candidates(self) -> tuple[Gene, ...]:
        """Absent child slots below the maximum tree depth.

        Candidate enumeration is a reconstructed executable interpretation of the
        source's local 'add a branch where one is absent' description.
        """

        candidates: list[Gene] = []
        parents = [()] + sorted(self.nodes)
        for parent in parents:
            if len(parent) >= self.max_memory:
                continue
            present_states = {child[-1] for child in self.children(parent)}
            for state in range(8):
                if state not in present_states:
                    candidates.append(parent + (state,))
        return tuple(candidates)

    @property
    def point_remove_candidates(self) -> tuple[Gene, ...]:
        return self.leaves

    @property
    def dupli_candidates(self) -> tuple[Gene, ...]:
        return tuple(leaf for leaf in self.leaves if len(leaf) < self.max_memory)

    @property
    def recursive_remove_candidates(self) -> tuple[Gene, ...]:
        return tuple(sorted(self.nodes))

    def point_add(self, branch: Sequence[int]) -> "Chromosome":
        branch_path = tuple(branch)
        if branch_path not in self.point_add_candidates:
            raise ValueError("branch is not a valid PointAdd candidate")
        return Chromosome(
            self.initial_action,
            self.nodes | {branch_path},
            self.max_memory,
        )

    def point_remove(self, leaf: Sequence[int]) -> "Chromosome":
        leaf_path = tuple(leaf)
        if leaf_path not in self.point_remove_candidates:
            raise ValueError("PointRemove can remove terminal branches only")
        return Chromosome(
            self.initial_action,
            self.nodes - {leaf_path},
            self.max_memory,
        )

    def dupli(self, leaf: Sequence[int]) -> "Chromosome":
        """Attach all eight children to one terminal node."""

        leaf_path = tuple(leaf)
        if leaf_path not in self.dupli_candidates:
            raise ValueError("Dupli requires a terminal below max_memory")
        children = {leaf_path + (state,) for state in range(8)}
        return Chromosome(
            self.initial_action,
            self.nodes | children,
            self.max_memory,
        )

    def remove_recursively(self, node: Sequence[int]) -> "Chromosome":
        """Delete one branch and every descendant beyond it."""

        node_path = tuple(node)
        if node_path not in self.nodes:
            raise ValueError("recursive-removal node is not present")
        remaining = {
            candidate
            for candidate in self.nodes
            if not _is_prefix(node_path, candidate)
        }
        return Chromosome(
            self.initial_action,
            frozenset(remaining),
            self.max_memory,
        )

    def mutate(
        self,
        rng: Random,
        rates: MutationRates = MutationRates(),
    ) -> "Chromosome":
        """Apply one mutation pass using the four historical local mechanisms.

        The sources recover the four operators and local rates but not an unambiguous
        global order when several operators fire in one generation. The order used
        here is therefore explicitly RECONSTRUCTED and named by
        ``RECONSTRUCTED_MUTATION_ORDER``. Within each operator, candidate events are
        sampled from one snapshot and applied simultaneously so ordering among
        candidates of the same operator cannot affect the result.
        """

        chromosome = self

        additions = {
            candidate
            for candidate in chromosome.point_add_candidates
            if rng.random() < rates.point_add
        }
        if additions:
            chromosome = Chromosome(
                chromosome.initial_action,
                chromosome.nodes | additions,
                chromosome.max_memory,
            )

        removals = {
            candidate
            for candidate in chromosome.point_remove_candidates
            if rng.random() < rates.point_remove
        }
        if removals:
            chromosome = Chromosome(
                chromosome.initial_action,
                chromosome.nodes - removals,
                chromosome.max_memory,
            )

        duplications = {
            candidate
            for candidate in chromosome.dupli_candidates
            if rng.random() < rates.dupli
        }
        if duplications:
            new_nodes = set(chromosome.nodes)
            for leaf in duplications:
                new_nodes.update(leaf + (state,) for state in range(8))
            chromosome = Chromosome(
                chromosome.initial_action,
                frozenset(new_nodes),
                chromosome.max_memory,
            )

        recursive_removals = {
            candidate
            for candidate in chromosome.recursive_remove_candidates
            if rng.random() < rates.remove_recursively
        }
        if recursive_removals:
            remaining = {
                node
                for node in chromosome.nodes
                if not any(_is_prefix(cut, node) for cut in recursive_removals)
            }
            chromosome = Chromosome(
                chromosome.initial_action,
                frozenset(remaining),
                chromosome.max_memory,
            )

        return chromosome

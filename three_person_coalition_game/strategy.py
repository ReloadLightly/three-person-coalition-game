"""Finite-history strategy semantics for the Akiyama–Kaneko model.

The historical model stores a strategy as an 8-ary tree assembled from ``genes``:
finite sequences of prior round states. For action selection, the source extracts the
maximal genes, reads history from most recent state backwards, and plays card 1
(white) when a gene and the available history are prefix-compatible; otherwise it
plays card 0 (black). The first-round action is stored separately by the strategy.

This module preserves those decision semantics while representing the tree by its
maximal gene paths. Explicit tree mutation is deliberately deferred to M3.
"""

from dataclasses import dataclass
from typing import Iterable, Sequence

from .game import Action


State = int
Gene = tuple[State, ...]


def _is_prefix(prefix: Sequence[int], sequence: Sequence[int]) -> bool:
    """Return whether ``prefix`` is a prefix of ``sequence``."""

    return len(prefix) <= len(sequence) and tuple(sequence[: len(prefix)]) == tuple(prefix)


def _canonical_genes(genes: Iterable[Sequence[int]]) -> tuple[Gene, ...]:
    """Return the source-equivalent set of maximal, non-overlapping gene paths.

    When one gene completely overlaps another from the root, the source keeps the
    longer path. Duplicate genes are collapsed. The resulting paths are sorted only
    to make the representation deterministic; order does not affect action choice.
    """

    normalized = {tuple(gene) for gene in genes}
    for gene in normalized:
        if not gene:
            raise ValueError("genes must contain at least one state")
        if any(state not in range(8) for state in gene):
            raise ValueError("gene states must be integers from 0 through 7")

    maximal = {
        gene
        for gene in normalized
        if not any(gene != other and _is_prefix(gene, other) for other in normalized)
    }
    return tuple(sorted(maximal))


@dataclass(frozen=True)
class Strategy:
    """A first action plus the maximal paths of an 8-ary finite-history strategy."""

    initial_action: Action
    genes: tuple[Gene, ...] = ()

    def __post_init__(self) -> None:
        if self.initial_action not in (0, 1):
            raise ValueError("initial_action must be 0 or 1")
        object.__setattr__(self, "genes", _canonical_genes(self.genes))

    @classmethod
    def from_genes(cls, initial_action: Action, genes: Iterable[Sequence[int]]) -> "Strategy":
        """Construct a strategy from source-style gene sequences."""

        return cls(initial_action=initial_action, genes=tuple(tuple(g) for g in genes))

    @property
    def memory_length(self) -> int:
        """Longest gene length represented by this strategy."""

        return max((len(gene) for gene in self.genes), default=0)

    def action(self, history: Sequence[State]) -> Action:
        """Choose the next action from prior focal-player states.

        ``history`` is supplied in normal chronological order (oldest to newest).
        The historical algorithm constructs B in the opposite order: one round ago,
        two rounds ago, and so forth. If either B or any maximal gene is a prefix of
        the other, the strategy plays 1 (white); otherwise it plays 0 (black).
        With no prior round, the separately encoded ``initial_action`` is used.
        """

        if any(state not in range(8) for state in history):
            raise ValueError("history states must be integers from 0 through 7")
        if not history:
            return self.initial_action

        recent_first = tuple(reversed(history))
        for gene in self.genes:
            if _is_prefix(gene, recent_first) or _is_prefix(recent_first, gene):
                return 1
        return 0

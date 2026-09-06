"""Historical population ecology for the three-person coalition model.

This module implements the source-recovered M3 mechanisms only:

* ordered species-triple interaction payoff ``g_ijk``;
* population-weighted species scores ``s_i``;
* population mean and relative fitness;
* replicator-like growth with historical baseline ``d = 0.2``;
* extinction of below-average species below ``KillLimit = 0.2``.

Species birth from mutation and random historical initialization are intentionally not
implemented here yet; they remain the next bounded reconstruction step.
"""

from dataclasses import dataclass
from math import isclose
from typing import Mapping, Sequence

from .interaction import play_interaction
from .strategy import Strategy


HISTORICAL_ROUNDS = 1000
HISTORICAL_GROWTH_CONSTANT = 0.2
HISTORICAL_KILL_LIMIT = 0.2

Triple = tuple[int, int, int]
FitnessTensor = dict[Triple, float]


def _validate_frequencies(frequencies: Sequence[float]) -> tuple[float, ...]:
    values = tuple(float(value) for value in frequencies)
    if not values:
        raise ValueError("at least one species frequency is required")
    if any(value < 0.0 for value in values):
        raise ValueError("species frequencies must be non-negative")
    if not isclose(sum(values), 1.0, rel_tol=1e-9, abs_tol=1e-12):
        raise ValueError("species frequencies must sum to 1")
    return values


def ordered_focal_payoff(
    focal: Strategy,
    left: Strategy,
    right: Strategy,
    rounds: int = HISTORICAL_ROUNDS,
) -> float:
    """Return ``g_ijk``: focal average payoff per round for an ordered triple."""

    if rounds <= 0:
        raise ValueError("rounds must be positive")
    records = play_interaction((focal, left, right), rounds=rounds)
    return sum(record.payoffs[0] for record in records) / rounds


def fitness_tensor(
    strategies: Sequence[Strategy],
    rounds: int = HISTORICAL_ROUNDS,
) -> FitnessTensor:
    """Evaluate every ordered focal/left/right species triple, including self-play."""

    if not strategies:
        raise ValueError("at least one strategy is required")
    if rounds <= 0:
        raise ValueError("rounds must be positive")

    tensor: FitnessTensor = {}
    for i, focal in enumerate(strategies):
        for j, left in enumerate(strategies):
            for k, right in enumerate(strategies):
                tensor[(i, j, k)] = ordered_focal_payoff(
                    focal,
                    left,
                    right,
                    rounds=rounds,
                )
    return tensor


def species_scores(
    strategies: Sequence[Strategy],
    frequencies: Sequence[float],
    rounds: int = HISTORICAL_ROUNDS,
    tensor: Mapping[Triple, float] | None = None,
) -> tuple[float, ...]:
    """Compute ``s_i = sum_jk g_ijk x_j x_k`` for all species."""

    if len(strategies) != len(frequencies):
        raise ValueError("strategies and frequencies must have the same length")
    weights = _validate_frequencies(frequencies)
    payoff_tensor = dict(tensor) if tensor is not None else fitness_tensor(strategies, rounds)

    expected_keys = {
        (i, j, k)
        for i in range(len(strategies))
        for j in range(len(strategies))
        for k in range(len(strategies))
    }
    if set(payoff_tensor) != expected_keys:
        raise ValueError("fitness tensor must contain every ordered species triple exactly once")

    scores: list[float] = []
    for i in range(len(strategies)):
        score = 0.0
        for j, x_j in enumerate(weights):
            for k, x_k in enumerate(weights):
                score += payoff_tensor[(i, j, k)] * x_j * x_k
        scores.append(score)
    return tuple(scores)


@dataclass(frozen=True)
class PopulationUpdate:
    """One transparent population-selection step, before mutant species are added."""

    frequencies: tuple[float, ...]
    mean_score: float
    fitness: tuple[float, ...]
    extinct: tuple[int, ...]


def update_population(
    frequencies: Sequence[float],
    scores: Sequence[float],
    growth_constant: float = HISTORICAL_GROWTH_CONSTANT,
    kill_limit: float = HISTORICAL_KILL_LIMIT,
) -> PopulationUpdate:
    """Apply relative-fitness growth, extinction, and normalization.

    The source states that a below-average species is removed when its population
    falls below ``KillLimit``. This implementation evaluates that condition after
    the source-defined growth step and before final survivor normalization. That
    timing is an explicit reconstruction detail, not a new causal mechanism.
    """

    weights = _validate_frequencies(frequencies)
    values = tuple(float(score) for score in scores)
    if len(values) != len(weights):
        raise ValueError("scores and frequencies must have the same length")
    if growth_constant < 0.0:
        raise ValueError("growth_constant must be non-negative")
    if not 0.0 <= kill_limit <= 1.0:
        raise ValueError("kill_limit must lie in [0, 1]")

    mean_score = sum(weight * score for weight, score in zip(weights, values))
    fitness = tuple(score - mean_score for score in values)
    grown = tuple(
        weight + growth_constant * relative * weight
        for weight, relative in zip(weights, fitness)
    )

    if any(value < -1e-12 for value in grown):
        raise ValueError("population update produced a negative species frequency")

    extinct = tuple(
        index
        for index, (grown_frequency, score) in enumerate(zip(grown, values))
        if score < mean_score and grown_frequency < kill_limit
    )
    surviving = tuple(
        0.0 if index in extinct else max(0.0, grown_frequency)
        for index, grown_frequency in enumerate(grown)
    )
    total = sum(surviving)
    if total <= 0.0:
        raise ValueError("population update eliminated every species")

    normalized = tuple(value / total for value in surviving)
    return PopulationUpdate(
        frequencies=normalized,
        mean_score=mean_score,
        fitness=fitness,
        extinct=extinct,
    )

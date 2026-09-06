"""Historical population ecology for the three-person coalition model.

This module implements the source-recovered ecological mechanisms:

* two positional seatings for each three-player matchup;
* population-weighted species scores ``s_i``;
* population mean and relative fitness;
* replicator-like growth with historical baseline ``d = 0.2``;
* extinction of below-average species below ``KillLimit = 0.2``.

M3b exposes the pre-normalization selection step because the historical source
places mutation after growth/extinction and normalizes only after mutation transfer.
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


def historical_focal_payoff(
    focal: Strategy,
    left: Strategy,
    right: Strategy,
    rounds: int = HISTORICAL_ROUNDS,
) -> float:
    """Return focal average payoff across the two historical partner seatings.

    Akiyama's detailed description says that a trio first plays ``max-round`` in
    one positional order, then two players exchange places and the trio plays
    ``max-round`` again. Histories restart between the two interactions.
    """

    if rounds <= 0:
        raise ValueError("rounds must be positive")

    first = play_interaction((focal, left, right), rounds=rounds)
    second = play_interaction((focal, right, left), rounds=rounds)
    focal_total = sum(record.payoffs[0] for record in first) + sum(
        record.payoffs[0] for record in second
    )
    return focal_total / (2 * rounds)


def ordered_focal_payoff(
    focal: Strategy,
    left: Strategy,
    right: Strategy,
    rounds: int = HISTORICAL_ROUNDS,
) -> float:
    """Compatibility name for the historical two-seating focal payoff."""

    return historical_focal_payoff(focal, left, right, rounds=rounds)


def fitness_tensor(
    strategies: Sequence[Strategy],
    rounds: int = HISTORICAL_ROUNDS,
) -> FitnessTensor:
    """Evaluate every focal/left/right species triple, including self-play.

    Entries retain the ordered ``(i,j,k)`` indexing used by the ecological score,
    while each matchup itself is averaged over the source-required swap of the two
    partner positions.
    """

    if not strategies:
        raise ValueError("at least one strategy is required")
    if rounds <= 0:
        raise ValueError("rounds must be positive")

    tensor: FitnessTensor = {}
    for i, focal in enumerate(strategies):
        for j, left in enumerate(strategies):
            for k, right in enumerate(strategies):
                tensor[(i, j, k)] = historical_focal_payoff(
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
class SelectionStep:
    """Growth/extinction result before the source's final normalization."""

    frequencies: tuple[float, ...]
    mean_score: float
    fitness: tuple[float, ...]
    extinct: tuple[int, ...]


@dataclass(frozen=True)
class PopulationUpdate:
    """Backward-compatible normalized population-selection result."""

    frequencies: tuple[float, ...]
    mean_score: float
    fitness: tuple[float, ...]
    extinct: tuple[int, ...]


def selection_step(
    frequencies: Sequence[float],
    scores: Sequence[float],
    growth_constant: float = HISTORICAL_GROWTH_CONSTANT,
    kill_limit: float = HISTORICAL_KILL_LIMIT,
) -> SelectionStep:
    """Apply relative-fitness growth and extinction without normalizing.

    The source describes growth, extinction, then mutation, and only after those
    operations normalization to total population 1. M3b therefore exposes the
    intermediate unnormalized masses required for faithful generation ordering.
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
    fitness = tuple(
        0.0
        if isclose(score, mean_score, rel_tol=1e-12, abs_tol=1e-12)
        else score - mean_score
        for score in values
    )
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
    if sum(surviving) <= 0.0:
        raise ValueError("population update eliminated every species")

    return SelectionStep(
        frequencies=surviving,
        mean_score=mean_score,
        fitness=fitness,
        extinct=extinct,
    )


def update_population(
    frequencies: Sequence[float],
    scores: Sequence[float],
    growth_constant: float = HISTORICAL_GROWTH_CONSTANT,
    kill_limit: float = HISTORICAL_KILL_LIMIT,
) -> PopulationUpdate:
    """Apply selection/extinction and normalize, preserving the M3a API."""

    step = selection_step(
        frequencies,
        scores,
        growth_constant=growth_constant,
        kill_limit=kill_limit,
    )
    total = sum(step.frequencies)
    normalized = tuple(value / total for value in step.frequencies)
    return PopulationUpdate(
        frequencies=normalized,
        mean_score=step.mean_score,
        fitness=step.fitness,
        extinct=step.extinct,
    )

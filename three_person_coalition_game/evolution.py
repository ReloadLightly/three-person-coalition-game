"""Generation integration for the historical three-person coalition ecology.

Source-anchored generation-level mechanisms include six random memory-1 starting
species with equal population, relative-fitness selection/extinction, four local tree
mutations, 10% parent-to-mutant transfer, normalization after mutation, and a maximum
of nine species. Low-level choices not preserved in the sources remain explicitly
Reconstructed.
"""

from dataclasses import dataclass
from math import isclose
from random import Random
from typing import Sequence

from .chromosome import Chromosome, MutationRates
from .ecology import (
    HISTORICAL_GROWTH_CONSTANT,
    HISTORICAL_KILL_LIMIT,
    HISTORICAL_ROUNDS,
    PayoffCache,
    selection_step,
    species_scores,
)


HISTORICAL_INITIAL_SPECIES = 6
HISTORICAL_MAX_SPECIES = 9
HISTORICAL_MUTANT_SHARE = 0.10

RECONSTRUCTED_INITIAL_BRANCH_PROBABILITY = 0.5
RECONSTRUCTED_INITIAL_ACTION_PROBABILITY = 0.5
RECONSTRUCTED_CAP_RULE = "block_novel_mutant_when_full"
RECONSTRUCTED_MUTATION_SCHEDULER = "one_local_mutation_pass_per_surviving_species"


@dataclass(frozen=True)
class PopulationState:
    """A normalized population of distinct strategy chromosomes."""

    chromosomes: tuple[Chromosome, ...]
    frequencies: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.chromosomes:
            raise ValueError("population must contain at least one species")
        if len(self.chromosomes) != len(self.frequencies):
            raise ValueError("chromosomes and frequencies must have the same length")
        if any(value < 0.0 for value in self.frequencies):
            raise ValueError("species frequencies must be non-negative")
        if not isclose(sum(self.frequencies), 1.0, rel_tol=1e-9, abs_tol=1e-12):
            raise ValueError("species frequencies must sum to 1")
        if len(set(self.chromosomes)) != len(self.chromosomes):
            raise ValueError("identical chromosomes belong to one species")


@dataclass(frozen=True)
class MutationEvent:
    """One mutation proposal and its population-bookkeeping outcome."""

    parent_index: int
    mutant: Chromosome
    outcome: str
    recipient_index: int | None = None


@dataclass(frozen=True)
class GenerationAudit:
    """Transparent record of one generation transition."""

    before: PopulationState
    scores: tuple[float, ...]
    mean_score: float
    fitness: tuple[float, ...]
    extinct: tuple[int, ...]
    mutation_events: tuple[MutationEvent, ...]
    after: PopulationState


def random_memory_one_chromosome(
    rng: Random,
    branch_probability: float = RECONSTRUCTED_INITIAL_BRANCH_PROBABILITY,
    action_probability: float = RECONSTRUCTED_INITIAL_ACTION_PROBABILITY,
) -> Chromosome:
    """Sample one Reconstructed random memory-1 starting chromosome."""

    if not 0.0 <= branch_probability <= 1.0:
        raise ValueError("branch_probability must lie in [0, 1]")
    if not 0.0 <= action_probability <= 1.0:
        raise ValueError("action_probability must lie in [0, 1]")

    initial_action = 1 if rng.random() < action_probability else 0
    genes = tuple(
        (state,)
        for state in range(8)
        if rng.random() < branch_probability
    )
    return Chromosome.from_genes(initial_action, genes)


def historical_initial_population(rng: Random) -> PopulationState:
    """Create six distinct random memory-1 species, each with population ``1/6``."""

    species: list[Chromosome] = []
    attempts = 0
    while len(species) < HISTORICAL_INITIAL_SPECIES:
        attempts += 1
        if attempts > 10_000:
            raise RuntimeError("could not sample six distinct initial species")
        candidate = random_memory_one_chromosome(rng)
        if candidate not in species:
            species.append(candidate)

    frequency = 1.0 / HISTORICAL_INITIAL_SPECIES
    return PopulationState(
        chromosomes=tuple(species),
        frequencies=(frequency,) * HISTORICAL_INITIAL_SPECIES,
    )


def _normalize(
    chromosomes: Sequence[Chromosome],
    masses: Sequence[float],
) -> PopulationState:
    pairs = [
        (chromosome, float(mass))
        for chromosome, mass in zip(chromosomes, masses)
        if mass > 0.0
    ]
    if not pairs:
        raise ValueError("population has no positive mass")

    total = sum(mass for _, mass in pairs)
    return PopulationState(
        chromosomes=tuple(chromosome for chromosome, _ in pairs),
        frequencies=tuple(mass / total for _, mass in pairs),
    )


def generation_step(
    population: PopulationState,
    rng: Random,
    rounds: int = HISTORICAL_ROUNDS,
    rates: MutationRates = MutationRates(),
    growth_constant: float = HISTORICAL_GROWTH_CONSTANT,
    kill_limit: float = HISTORICAL_KILL_LIMIT,
    max_species: int = HISTORICAL_MAX_SPECIES,
    mutant_share: float = HISTORICAL_MUTANT_SHARE,
    payoff_cache: PayoffCache | None = None,
) -> GenerationAudit:
    """Execute one historical-style generation and return its complete audit.

    ``payoff_cache`` is an optional exact acceleration for multi-generation runs:
    deterministic matchup payoffs depend on strategies, not population frequencies,
    so previously evaluated triples can be reused without changing the experiment.
    """

    if max_species < 1:
        raise ValueError("max_species must be positive")
    if not 0.0 <= mutant_share <= 1.0:
        raise ValueError("mutant_share must lie in [0, 1]")

    strategies = tuple(chromosome.to_strategy() for chromosome in population.chromosomes)
    scores = species_scores(
        strategies,
        population.frequencies,
        rounds=rounds,
        payoff_cache=payoff_cache,
    )
    selection = selection_step(
        population.frequencies,
        scores,
        growth_constant=growth_constant,
        kill_limit=kill_limit,
    )

    survivors = [
        chromosome
        for index, chromosome in enumerate(population.chromosomes)
        if index not in selection.extinct
    ]
    masses = [
        mass
        for index, mass in enumerate(selection.frequencies)
        if index not in selection.extinct
    ]

    initial_survivor_count = len(survivors)
    proposals = [
        survivors[index].mutate(rng, rates)
        for index in range(initial_survivor_count)
    ]
    base_masses = tuple(masses)
    events: list[MutationEvent] = []

    for parent_index, mutant in enumerate(proposals):
        parent = survivors[parent_index]
        if mutant == parent:
            events.append(MutationEvent(parent_index, mutant, "unchanged", parent_index))
            continue

        transfer = base_masses[parent_index] * mutant_share
        if mutant in survivors:
            recipient = survivors.index(mutant)
            masses[parent_index] -= transfer
            masses[recipient] += transfer
            events.append(MutationEvent(parent_index, mutant, "merged", recipient))
        elif len(survivors) < max_species:
            masses[parent_index] -= transfer
            survivors.append(mutant)
            masses.append(transfer)
            recipient = len(survivors) - 1
            events.append(MutationEvent(parent_index, mutant, "new", recipient))
        else:
            events.append(MutationEvent(parent_index, mutant, "blocked_at_cap", None))

    after = _normalize(survivors, masses)
    return GenerationAudit(
        before=population,
        scores=scores,
        mean_score=selection.mean_score,
        fitness=selection.fitness,
        extinct=selection.extinct,
        mutation_events=tuple(events),
        after=after,
    )

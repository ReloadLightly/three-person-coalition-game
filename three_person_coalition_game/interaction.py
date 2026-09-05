"""Deterministic repeated interaction for three finite-history strategies."""

from dataclasses import dataclass
from typing import Sequence

from .game import Action, RoundState
from .strategy import Strategy


@dataclass(frozen=True)
class InteractionRound:
    """One synchronous round in global player order (player 1, 2, 3)."""

    actions: tuple[Action, Action, Action]
    states: tuple[int, int, int]
    payoffs: tuple[int, int, int]


def focal_states(actions: Sequence[Action]) -> tuple[RoundState, RoundState, RoundState]:
    """Return each player's left/right/self state from global counter-clockwise order.

    The source places players 1, 2, 3 counter-clockwise. For player ``i``, the left
    neighbour is ``i+1`` and the right neighbour is ``i-1`` modulo three.
    """

    if len(actions) != 3:
        raise ValueError("exactly three actions are required")
    a = tuple(actions)
    return tuple(
        RoundState(left=a[(i + 1) % 3], right=a[(i - 1) % 3], self_=a[i])
        for i in range(3)
    )  # type: ignore[return-value]


def play_interaction(strategies: Sequence[Strategy], rounds: int) -> tuple[InteractionRound, ...]:
    """Play one fixed-position synchronous interaction for ``rounds`` rounds."""

    if len(strategies) != 3:
        raise ValueError("exactly three strategies are required")
    if rounds < 0:
        raise ValueError("rounds must be non-negative")

    histories: list[list[int]] = [[], [], []]
    records: list[InteractionRound] = []

    for _ in range(rounds):
        actions = tuple(strategies[i].action(histories[i]) for i in range(3))
        states = focal_states(actions)
        state_ids = tuple(state.index for state in states)
        payoffs = tuple(state.payoffs[2] for state in states)

        records.append(InteractionRound(actions=actions, states=state_ids, payoffs=payoffs))
        for i, state_id in enumerate(state_ids):
            histories[i].append(state_id)

    return tuple(records)

"""Faithful reconstruction of the three-person coalition game."""

from .game import RoundState
from .interaction import InteractionRound, focal_states, play_interaction
from .strategy import Gene, Strategy

__all__ = [
    "Gene",
    "InteractionRound",
    "RoundState",
    "Strategy",
    "focal_states",
    "play_interaction",
]

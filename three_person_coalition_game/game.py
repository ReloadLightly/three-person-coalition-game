"""Deterministic stage game from Akiyama & Kaneko's three-person model."""

from dataclasses import dataclass


Action = int
Payoffs = tuple[int, int, int]


@dataclass(frozen=True)
class RoundState:
    """One round from the focal player's left/right/self perspective."""

    left: Action
    right: Action
    self_: Action

    def __post_init__(self) -> None:
        if any(action not in (0, 1) for action in self.actions):
            raise ValueError("actions must be 0 or 1")

    @property
    def actions(self) -> tuple[Action, Action, Action]:
        return (self.left, self.right, self.self_)

    @property
    def index(self) -> int:
        """Source state number: binary digits are (left, right, self)."""

        return 4 * self.left + 2 * self.right + self.self_

    @property
    def payoffs(self) -> Payoffs:
        """Return payoffs in (left, right, self) order."""

        if self.left == self.right == self.self_:
            return (0, 0, 0)

        majority_action = 1 if sum(self.actions) == 2 else 0
        return tuple(3 if action == majority_action else 0 for action in self.actions)  # type: ignore[return-value]

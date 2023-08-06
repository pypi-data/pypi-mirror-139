from typing import Tuple

import torch

import torchaddons
from torchaddons import distributions


class Categorical(distributions.Base):
    """Categorical distribution."""

    def __init__(self, probabilities: torch.Tensor) -> None:
        """Creates a categorical distribution.

        Args:
            probabilities (torch.Tensor): Probabilities (or relative probability) along
                the last dimension. Must be non-negative.
        """
        super().__init__()
        if (probabilities < 0).any():
            raise ValueError("Probabilities must be non-negative.")
        self._probs = probabilities / probabilities.sum(-1, True)

    @property
    def is_continuous(self) -> bool:
        return False

    @property
    def is_discrete(self) -> bool:
        return True

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._probs.shape[:-1]

    def clone(self) -> "distributions.Categorical":
        return Categorical(self._probs.clone())

    @property
    def probabilities(self) -> torch.Tensor:
        """Probabilities of the categories."""
        return self._probs

    def sample(self, *shape: Tuple[int, ...]) -> torch.Tensor:
        return torchaddons.random.choice(self._probs.expand(shape + self._probs.shape))

    def _include_discrete_mask(self, mask: distributions.constraints.CategoricalMask):
        if mask.mask.shape != self._probs.shape:
            raise ValueError("Discrete mask does not match the shape of the distribution.")
        
        self._probs[~mask.mask] = 0.0
        self._probs /= self._probs.sum(-1, keepdim=True)

    def include_constraint(self, constraint: distributions.constraints.Base) -> bool:
        if isinstance(constraint, distributions.constraints.CategoricalMask):
            self._include_discrete_mask(constraint)
            return True
        return super().include_constraint(constraint)

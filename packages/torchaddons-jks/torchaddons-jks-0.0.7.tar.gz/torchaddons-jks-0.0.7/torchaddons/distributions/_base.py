import abc
from typing import Tuple

import torch

from torchaddons import distributions
from . import constraints


class Base(abc.ABC):
    """Base class for distributions."""

    @property
    @abc.abstractmethod
    def is_continuous(self) -> bool:
        """True if the distribution is continuous."""
        pass

    @property
    @abc.abstractmethod
    def is_discrete(self) -> bool:
        """True if the distribution is discrete."""
        pass

    @abc.abstractmethod
    def sample(self, *shape: Tuple[int, ...]) -> torch.Tensor:
        """Samples the distribution.

        Args:
            shape (Tuple[int, ...]): Batch dimensions to prepend to the output. Defaults
                to none. If the distribution was parametrized using batch data, then
                this argument prepends _further_ batches.

        Returns:
            torch.Tensor: Random sample.
        """
        pass

    @property
    @abc.abstractmethod
    def shape(self) -> Tuple[int, ...]:
        """Shape of the output, if called with no extra batch dimensions."""
        pass

    @abc.abstractmethod
    def clone(self) -> "distributions.Base":
        pass

    def include_constraint(self, constraint: constraints.Base) -> bool:
        """Constraints should not be added by calling this method. Instead, call
        `constraint.apply_to(distribution)`.

        Args:
            constraint (constraints.Base): Constraint to include.

        Returns:
            bool: True if the constraint was successfully included, otherwise False.
        """
        if isinstance(self, distributions.RejectionSampler):
            self.add_constraint(constraint)
            return True
        return False

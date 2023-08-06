from typing import Tuple
import functools

import torch

from torchaddons import distributions


class RejectionSampler(distributions.Base):
    """Distribution with constraints that are evaluated using rejection sampling."""

    def __init__(
        self,
        distribution: distributions.Base,
        *constraints: distributions.constraints.Base
    ) -> None:
        """Creates a rejection sampler.

        Args:
            distribution (distributions.Base): Underlying distribution.
            constraints (distributions.constraints.Base): Constraints to apply.
        """
        super().__init__()
        self._distribution = distribution
        self._constraints = list(constraints)

    @property
    def is_continuous(self) -> bool:
        return self._distribution.is_continuous

    @property
    def is_discrete(self) -> bool:
        return self._distribution.is_discrete

    def add_constraint(self, constraint: distributions.constraints.Base):
        """Adds a constraint to the rejection sampling.

        Args:
            constraint (distributions.constraints.Base): Constraint to add.
        """
        self._constraints.append(constraint)

    def sample(self, *shape: Tuple[int, ...]) -> torch.Tensor:
        def get_reducer(value: torch.Tensor):
            def reducer(
                mask: torch.Tensor, constraint: distributions.constraints.Base
            ) -> torch.Tensor:
                return mask & constraint.check(value)

            return reducer

        value = self._distribution.sample(*shape)
        inv_mask = ~functools.reduce(
            get_reducer(value),
            self._constraints,
            torch.ones(shape, dtype=torch.bool, device=value.device),
        )
        while inv_mask.any():
            value[inv_mask] = self._distribution.sample(inv_mask.sum())
            inv_mask[inv_mask.clone()] = ~ functools.reduce(
                get_reducer(value[inv_mask]),
                self._constraints,
                torch.ones(inv_mask.sum(), dtype=torch.bool, device=value.device),
            )
        return value

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._distribution.shape

    def clone(self) -> "RejectionSampler":
        return RejectionSampler(
            self._distribution.clone(), *(x.clone() for x in self._constraints)
        )

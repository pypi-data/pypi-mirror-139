import torch

from torchaddons.distributions import constraints


class UpperBound(constraints.LowerBound):
    """Upper bound constraint."""

    def check(self, value: torch.Tensor) -> torch.Tensor:
        return super().check(-value)

    def clone(self) -> "constraints.UpperBound":
        return UpperBound(
            self.bound.clone(),
            self.allow_equal
        )

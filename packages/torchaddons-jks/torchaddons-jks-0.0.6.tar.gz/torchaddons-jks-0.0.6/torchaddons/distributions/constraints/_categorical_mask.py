import torch
from torchaddons import distributions
from torchaddons.distributions import constraints


class CategoricalMask(constraints.Base):
    def __init__(self, mask: torch.Tensor) -> None:
        super().__init__()
        self._mask = mask

    def check(self, value: torch.Tensor) -> torch.Tensor:
        # This method is not yet implemented as it is easy to simply apply the mask
        # to a distribution and get a closed form expression for the masked
        # distribution. If you need this, you are very welcome to make a pull request.
        raise NotImplementedError

    @property
    def mask(self) -> torch.Tensor:
        """Boolean mask"""
        return self._mask

    def clone(self) -> "distributions.constraints.CategoricalMask":
        return CategoricalMask(self._mask.clone())

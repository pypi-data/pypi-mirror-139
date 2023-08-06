from typing import Tuple

import torch

from torchaddons import distributions


class Normal(distributions.Base):
    def __init__(self, mean: torch.Tensor, cov: torch.Tensor) -> None:
        super().__init__()
        self._mean = mean
        self._cov = cov
        self._d = torch.distributions.MultivariateNormal(mean, cov)

    def sample(self, *shape: Tuple[int, ...]) -> torch.Tensor:
        return self._d.sample(shape)

    def clone(self) -> "distributions.Normal":
        return Normal(
            self._mean.clone(),
            self._cov.clone()
        )
    
    @property
    def is_continuous(self) -> bool:
        return True

    @property
    def is_discrete(self) -> bool:
        return False

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._mean.shape

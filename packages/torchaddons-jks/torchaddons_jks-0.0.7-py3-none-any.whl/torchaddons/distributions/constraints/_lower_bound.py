import torch

from torchaddons.distributions import constraints


class LowerBound(constraints.Base):
    """Lower bound constraint."""
    def __init__(self, bound: torch.Tensor, allow_equal: bool = True) -> None:
        """
        Args:
            bound (torch.Tensor): Bound.
            allow_equal (bool, optional): If True, equal values are allowed. Defaults
                to True.
        """
        super().__init__()
        self._bound = bound
        self._allow_equal = allow_equal
        self._scalar = len(bound.shape) == 0
        self._fn = torch.ge if allow_equal else torch.gt

    @property
    def dim(self) -> int:
        return 0 if self._scalar else self._bound.shape[-1]

    @property
    def bound(self) -> torch.Tensor:
        """Bound."""
        return self._bound

    @property
    def allow_equal(self) -> bool:
        """If True, equal values are allowed."""
        return self._allow_equal

    def check(self, value: torch.Tensor) -> torch.Tensor:
        if self._scalar:
            return self._fn(value, self._bound)
        return self._fn(value, self._bound).all(-1)

    def clone(self) -> "constraints.LowerBound":
        return LowerBound(
            self._bound.clone(),
            self._allow_equal
        )

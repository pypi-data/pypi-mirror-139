import torch
from torchaddons.distributions import constraints



class Empty(constraints.Base):
    """Constraint class imposing no constraints, only the dimension of the vector."""
    
    def __init__(self, dim: int) -> None:
        """
        Args:
            dim (int): Dimension of vectors.
        """
        super().__init__()
        self._dim = dim

    @property
    def dim(self) -> int:
        return self._dim

    def check(self, value: torch.Tensor) -> torch.Tensor:
        if value.shape[-1] != self._dim:
            return torch.zeros(value.shape[:-1], dtype=torch.bool, device=value.device)
        return torch.ones(value.shape[:-1], dtype=torch.bool, device=value.device)

    def clone(self) -> "Empty":
        return Empty(self._dim)

import torch
from torchaddons.distributions import constraints



class Empty(constraints.Base):
    """Constraint class imposing no constraints."""
    def check(self, value: torch.Tensor) -> torch.Tensor:
        return torch.ones(value.shape[:-1], dtype=torch.bool, device=value.device)

    def clone(self) -> "Empty":
        return Empty()

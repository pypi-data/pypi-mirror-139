import abc
import torch

from torchaddons import distributions


class Base(abc.ABC):
    """Base class for constraints."""
    
    @abc.abstractmethod
    def check(self, value: torch.Tensor) -> torch.Tensor:
        pass

    @property
    @abc.abstractmethod
    def dim(self) -> int:
        """Dimension of the constraint space."""
        pass

    def apply_to(self, distribution: "distributions.Base", allow_inplace: bool=True) -> "distributions.Base":
        """Applies the constraint to a distribution.

        Args:
            distribution (distributions.Base): distribution to apply.
            allow_inplace (bool): If True, this method will modifiy distributions in
                place if possible. Otherwise, a copy is made.

        Returns:
            distributions.Base: New distribution object respecting the given constraint.
                Note, this operation may edit certain distributions inplace.
        """
        if not allow_inplace:
            distribution = distribution.clone()

        if distribution.include_constraint(self):
            return distribution
        return distributions.RejectionSampler(distribution, self)

    @abc.abstractmethod
    def clone(self) -> "distributions.constraints.Base":
        """Clones the constraint.

        Returns:
            distributions.constraints.Base: Cloned object.
        """
        pass

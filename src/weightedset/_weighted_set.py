import math
from operator import itemgetter
from typing import Dict
from typing import Hashable
from typing import List
from typing import TypeVar

T = TypeVar("T", bound=Hashable)


class WeightedSet:
    """A set of unique keys with attached weights.

    The weights assigned to keys must be positive numbers. When weights for
    the same key are combined, then they are added together.

    This is a standalone class. However, it's interface is based on the
    interfaces for the `set` and `dict` builtin types.
    """

    def __init__(self):
        #: All keys in the weighted set, with their weights as the dictionary
        #: value
        self._weights: Dict[T, float] = {}

    def __contains__(self, item) -> bool:
        """Determine whether a key is in this set with a non-zero weight."""
        return item in self._weights

    def __getitem__(self, key: T) -> float:
        """Get the weight for a key in this set.

        Raises:
            KeyError if the key doesn't exist.
        """
        return self._weights[key]

    def __imul__(self, scale: float) -> "WeightedSet":
        """Scale all weights by the supplied factor."""
        if scale < 0:
            raise ValueError("Weights must be positive")

        scaled_weights = {}
        for key, weight in self._weights.items():
            new_weight = weight * scale
            if new_weight == 0:
                continue
            elif new_weight in (math.inf, math.nan):
                raise OverflowError(f"Some of the resulting weights were {new_weight}")

            scaled_weights[key] = new_weight

        self._weights = scaled_weights
        return self

    def __itruediv__(self, scale: float) -> "WeightedSet":
        """Scale all weights by the inverse of the supplied factor."""
        if scale == 0:
            raise ZeroDivisionError()
        if scale < 0:
            raise ValueError("Weights must be positive")

        scaled_weights = {}
        for key, weight in self._weights.items():
            new_weight = weight / scale
            if new_weight == 0:
                continue
            elif new_weight in (math.inf, math.nan):
                raise OverflowError(f"Some of the resulting weights were {new_weight}")

            scaled_weights[key] = new_weight

        self._weights = scaled_weights
        return self

    def add(self, key: T, weight: float = 1):
        """Add a key to this weighted set with the specified weight.

        If the key is already present, then it's weight is increased by the
        specified weight.
        """
        if weight < 0:
            raise ValueError("Weights must be positive")
        if weight == 0:
            # Ignore
            return

        if key in self:
            self._weights[key] += weight
        else:
            self._weights[key] = weight

    def clamp(self, limit: float):
        """Set the maximum value for weights currently in this weighted set.

        Any key with a weight greater than `limit` will have it's weight set
        to `limit`.

        There is no permanent restriction, so after clamping weights may become
        larger than `limit`.
        """
        if limit == 0:
            raise ValueError("Max weight should be non-zero")
        if limit < 0:
            raise ValueError("Max weight must be positive")

        # You can't modify a dictionary whilst iterating through it, so we
        # pull out the over-size keys in a first pass.
        oversize_keys = [key for key, weight in self._weights.items() if weight > limit]
        for key in oversize_keys:
            self._weights[key] = limit

    def copy(self) -> "WeightedSet":
        """Return a shallow copy of the weighted set."""
        newset = WeightedSet()
        newset._weights.update(self._weights)
        return newset

    def keys(self) -> List[T]:
        """Get an ordered list of keys in this weighted set, with the highest weighted item first."""
        return [
            keyword
            for keyword, weight in sorted(
                self._weights.items(), key=itemgetter(1), reverse=True
            )
        ]

    def max_weight(self) -> float:
        """The maximum weight in this weighted set."""
        return max(self._weights.values(), default=0)

    def update(self, *others: "WeightedSet"):
        """Update the weighted set in-place, adding all weights from all others."""
        for ws in others:
            if not isinstance(ws, WeightedSet):
                raise TypeError(
                    f"Can't update a {self.__class__.__name__} from a {type(ws)}"
                )

            for key in ws.keys():
                self.add(key, ws[key])

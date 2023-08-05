__all__ = ["Accumulator", "Accuracy"]


class Accumulator:
    """Object that stores running sum and average.

    Usage: 
    - Call the update function to add a value. 
    - Get running average by accessing the mean proporty, running sum by the total property, and
    number of values by the length property.
    """    
    def __init__(self) -> None:
        self._cumsum: float = 0.0
        self._length: int = 0

    def update(self, value: float, length: int = 1) -> None:
        """Add a value to the running sum.

        Args:
            value (float): The value to be added.
            length (int, optional): The input value is by default treated as a single value. 
                If it is a sum of multiple values, the number of values can be specified by this
                length argument, so that the running sum is calculated correctly. Defaults to 1.
        """        
        self._cumsum += float(value)
        self._length += int(length)

    @property
    def mean(self) -> float:
        if self._length > 0:
            return self._cumsum / self._length
        else:
            return 0.0

    @property
    def total(self) -> float:
        return self._cumsum

    @property
    def length(self) -> int:
        return self._length


class Accuracy:
    """Object that calculates and tracks accuracy between predictions and true labels.

    Usage: 
    - Call the update function to add predictions and labels. 
    - Get accuracy score at any point by accessing the value proporty.
    """    
    def __init__(self) -> None:
        self._cumsum: float = 0.0
        self._length: int = 0

    def update(self, preds, labels) -> None:
        """Add predictions and labels to be compared.

        Args:
            preds: Array of predicted labels.
            labels: Array of true labels.
        """        
        assert len(preds) == len(
            labels), "The list of predictions and the list of labels must have same length"
        self._cumsum += float((preds == labels).sum())
        self._length += len(labels)

    @property
    def value(self) -> float:
        if self._length > 0:
            return float(self._cumsum / self._length)
        else:
            return 0.0

from typing import Generator, List, Optional

from .exceptions import ExceedsMaximumValueError, NegativeRangeError, NoMaximumValueError, NoMinimumValueError


class SmartRange:
    """The class that represents a range of values. Input consists of a string containing the range.

    A range string is a comma-separated list of range items. There are 4 types of range items supported by the class:

    #. Classic range with a defined start and finish. Example: ``1-5``

       .. warning::
          Range items cannot have a negative difference between the start and finish values.

    #. Range with a defined start and an undefined finish. This requires the ``max_val`` parameter to be supplied to
       the :py:meth:`~SmartRange.__init__` method. This type of range can only show up once at the end of the range
       string. Example: ``1-``

    #. Range with an undefined start and a defined finish. If this item is the first range in the range string, it
       requires the ``min_val`` parameter to be supplied to the :py:meth:`~SmartRange.__init__` method. Otherwise,
       it will assume that the starting value is one more than the previous range item.

          * Example at the start of the range string with a defined ``min_val`` parameter: ``-5`` -> ``<min_val>-5``

          * Example where the range string is ``1-5,-8`` -> ``1-5,6-8``

    #. A plus symbol and a number. This will indicate a range where the end of the previous range plus one is the
       starting number, and the end of the range is the starting number plus the provided number minus one. If
       specified at the beginning of the range string, it requires the ``min_val`` parameter to be supplied to the
       :py:meth:`~SmartRange.__init__` method.

          * Example at the start of the range string with a defined ``min_val`` parameter: ``+5`` ->
            ``<min_val> - <min_val+5>``

          * Example where the range string is ``1-5,+8`` -> ``1-5,6-13``
    """

    ranges: List[range]
    r"""The list of :py:class:`range`\ s. Can be externally modified to add, change, or remove ranges."""

    def __init__(self, range_str: str, *, min_val: Optional[int] = None, max_val: Optional[int] = None):
        """
        Create a new :py:class:`SmartRange` object.

        :param range_str: The input range string.
        :type range_str: str
        :param min_val: The minimum value of the range. If not supplied, range items #2 and #4 cannot be supplied at
            the beginning of the range string.
        :type min_val: Optional[int]
        :param max_val: The maximum value of the range. If not supplied, range item #3 cannot be supplied at the
            end of the range string.

            .. warning::
               If a ``max_val`` is supplied, no item in the range string can have an end value greater than the
               value.
        :type max_val: Optional[int]
        :raises NoMinimumValueError: If a type 2 or 4 range item is used at the beginning of the range string and no
            ``min_val`` is supplied.
        :raises NoMaximumValueError: If a type 3 range item is used at the end of the range string and no ``max_val``
            is supplied.
        :raises NegativeRangeError: If a range item has a negative difference between the start and finish values.
        :raises ExceedsMaximumValueError: If ``max_val`` is provided and a range item has an end value greater than
            ``max_val``.
        """
        self.ranges = self._parse_range(range_str, min_val, max_val)

    def _parse_range(self, range_str: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> List[range]:
        parts = range_str.split(",")
        ranges = []
        locked_max = max_val
        current_max = min_val
        for part in parts:
            if not part.startswith("+"):
                start, sep, end = part.partition("-")
                start = int(start) if start else current_max
                if end:
                    end = int(end)
                else:
                    end = max_val
                    max_val = None
            else:
                start = current_max
                end = start + int(part[1:]) - 1
                # If we say +25, we want 25 numbers, not to end at the 25th index (26 numbers).
            if start is None:
                raise NoMinimumValueError(part)
            if end is None:
                raise NoMaximumValueError(part)
            if end < start:
                raise NegativeRangeError(start, end)
            if locked_max and max(start, end) > locked_max:
                raise ExceedsMaximumValueError(start, end, locked_max)
            ranges.append(range(start, end + 1))
            current_max = end + 1
        return ranges

    def __iter__(self) -> Generator[int, None, None]:
        """Returns a generator containing all of the numbers in the smart range.

        .. note::
            In order to iterate over the list of range objects, use the :py:attr:`ranges` attribute, such as:

            .. code-block:: python

                for range_obj in smart_range.ranges:
                    print(range_obj.start, range_obj.stop)
        """
        for r in self.ranges:
            yield from r

    def __len__(self) -> int:
        """Returns the total number of values in all the range items combined."""
        return sum(len(r) for r in self.ranges)

    def __contains__(self, item: int) -> bool:
        """Returns ``True`` if the number is in the range, ``False`` otherwise."""
        return any(item in r for r in self.ranges)

    def __repr__(self) -> str:
        """Returns a string representation of the range."""
        return ",".join(f"{r.start}-{r.stop - 1}" for r in self.ranges)

import collections
from enum import Enum
from abc import ABC, abstractmethod


class SortType(Enum):
    BY_FREQ = 0
    BY_ITEM = 1


def unique_copy(input_list):
    """
    Returns a list containing the unique elements from the input_list while preserving the original order.

    Args:
        input_list (list): The input list containing elements to be filtered for uniqueness.

    Returns:
        list: A new list containing unique elements in the same order as they appear in the input_list.

    Example:
        >>> input_list = [1, 2, 5, 2, 4, 4, 3, 5]
        >>> unique_elements = unique_copy(input_list)
        >>> print(unique_elements)
        [1, 2, 5, 4, 3]

    """
    unique_elements = []
    seen_elements = set()

    for item in input_list:
        if item not in seen_elements:
            unique_elements.append(item)
            seen_elements.add(item)

    return unique_elements


class FrequencyTable(ABC):
    def __init__(self, data):
        self._data = data
        self._table = self._calculate_frequencies()
        self._frequencies = list(self._table.values())

    @abstractmethod
    def _calculate_frequencies(self):
        pass

    @abstractmethod
    def display_table(self):
        pass

    def to_dict(self):
        return self._table.copy()

    def get_data(self):
        return self._data.copy()

    def get_frequencies(self):
        return self._frequencies.copy()

    def get_total(self):
        return sum(self._frequencies)

    def sort(self, by=SortType.BY_FREQ, acs=True):
        try:
            if not isinstance(by, SortType):
                raise ValueError("Invalid SortType selected. by must be either a SortType.BY_FREQ or SortType.BY_ITEM.")
        except ValueError as e:
            print(e)
        else:
            self._table = dict(sorted(self._table.items(), key=lambda item: item[by.value], reverse=not acs))

    def __len__(self):
        return len(self._data)


class DiscreteFrequencyTable(FrequencyTable):
    def __init__(self, data):
        super().__init__(data)

    def _calculate_frequencies(self):
        counter = collections.Counter(self._data)
        return dict(counter.items())

    def display_table(self):
        max_len = 0

        for class_item in self._table:
            max_len = max(max_len, len(str(class_item)))

        max_len += 10

        print(f"{'Class':<{max_len}}", "Frequency")
        for class_item in self._table:
            print(f"{class_item:<{max_len}}", self._table[class_item])


class EqualClassLengthFrequencyTable(FrequencyTable):
    def __init__(self, data: list[float], cut_points=None):
        super().__init__(data)
        self.num_classes = cut_points

    def _calculate_frequencies(self):
        pass

    def display_table(self):
        pass


class RelativeFrequencyTable(FrequencyTable):
    def _calculate_frequencies(self):
        pass

    def display_table(self):
        pass


class CumulativeFrequencyTable(FrequencyTable):
    def _calculate_frequencies(self):
        pass

    def display_table(self):
        pass

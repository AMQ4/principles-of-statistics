import collections
import heapq
from enum import Enum
from abc import ABC, abstractmethod
from typing import Callable, Any


class SortType(Enum):
    BY_ITEM = 0
    BY_FREQ = 1


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
    def __init__(self, data=None):
        self._table = self._calculate_frequencies(data if data is not None else [])

    @abstractmethod
    def _calculate_frequencies(self, data):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def mean(self):
        pass

    @abstractmethod
    def median(self):
        pass

    @abstractmethod
    def mode(self):
        pass

    def display_table(self):
        print(self.__str__())

    def to_dict(self):
        return self._table.copy()

    def get_data(self):
        return self._table.keys()

    def get_frequencies(self):
        return self._table.values()

    def get_total(self):
        return sum(self._table.values())

    def sort(self, by=SortType.BY_FREQ, acs=True):
        try:
            if not isinstance(by, SortType):
                raise ValueError("Invalid SortType selected. by must be either a SortType.BY_FREQ or SortType.BY_ITEM.")
        except ValueError as e:
            print(e)
        else:
            self._table = dict(sorted(self._table.items(), key=lambda item: item[by.value], reverse=not acs))

    def append(self, data_to_append):
        counter = collections.Counter(data_to_append)
        for item in counter:
            if item in self._table:
                self._table[item] += counter[item]
            else:
                self._table[item] = counter[item]

    def merge(self, freqtable: 'FrequencyTable'):
        for item, freq in freqtable._table.items():
            self.append([item] * freq)

    def filter_by_freq(self, min_frequency, max_frequency):
        freqrange = range(min_frequency, max_frequency + 1)
        freqtable = self.__class__()

        for item, freq in self._table.items():
            if freq in freqrange:
                freqtable.append([item] * freq)

        return freqtable

    def filter_by_class(self, predicate: Callable[[Any, Any], bool]):
        freqtable = self.__class__()
        for item, freq in self._table.items():
            if predicate(item, freq):
                freqtable.append([item] * freq)
        return freqtable

    def __len__(self):
        return len(self._table.keys())

    def get_subset(self, subset_elements):
        freqtable = self.__class__()
        for element in subset_elements:
            freq = self._table.get(element)
            freqtable.append([element] * (freq if freq is not None else 0))
        return freqtable

    def get_top_n_elements(self, n):
        freqtable = self.__class__()
        top_n_elements = heapq.nlargest(n, self._table.items(), lambda item: item[1])

        for item, freq in top_n_elements:
            freqtable.append([item] * freq)

        return freqtable

    def get_lowest_n_elements(self, n):
        freqtable = self.__class__()
        top_n_elements = heapq.nsmallest(n, self._table.items(), lambda item: item[1])

        for item, freq in top_n_elements:
            freqtable.append([item] * freq)

        return freqtable

    def map_elements(self, func: Callable[[Any], Any]):
        items = list(self._table.keys())
        for item in items:
            new_item = func(item)
            freq = self._table[item]
            self._table.pop(item)
            if self._table.get(new_item) is not None:
                self._table[new_item] += freq
            else:
                self._table[new_item] = freq

    def apply_frequency_operation(self, func: Callable[[Any], Any]):
        items_with_neg_freq = []
        for item, freq in self._table.items():
            newfreq = func(freq)
            try:
                if newfreq <= 0:
                    raise ValueError(f"{item} deleted since new frequency, {newfreq} <= 0")
            except ValueError as e:
                print(e)
                items_with_neg_freq.append(item)
            else:
                self._table[item] = newfreq

        for item in items_with_neg_freq:
            self._table.pop(item)


class DiscreteFrequencyTable(FrequencyTable):
    def __init__(self, data=None):
        super().__init__(data)

    def _calculate_frequencies(self, data):
        counter = collections.Counter(data)
        return dict(counter.items())

    def __str__(self):
        max_len = 0

        for class_item in self._table:
            max_len = max(max_len, len(str(class_item)))

        max_len += 10

        table = ""
        table = table + f"{'Class':<{max_len}}" + "Frequency"

        for class_item in self._table:
            table = table + f"\n{class_item:<{max_len}}" + str(self._table[class_item])

        return table

    def mean(self):
        sum = 0
        for item, freq in self._table.items():
            sum += item * freq

        return sum / self.get_total()

    def median(self):
        items = []
        for item, freq in self._table.items():
            items = items + [item] * freq

        items.sort()

        return items[int(self.get_total() / 2)] if self.get_total() % 2 == 1 else (
                (items[int(self.get_total() / 2)] + items[int(self.get_total() / 2) - 1]) / 2)

    def mode(self):
        return list(self.get_top_n_elements(1).get_data())[0]


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

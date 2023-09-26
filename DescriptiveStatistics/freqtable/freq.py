from collections.abc import Hashable
from enum import Enum
from abc import ABC, abstractmethod
from typing import Callable, Any, Iterable
from bisect import bisect_left
from random import random
import collections
import heapq


class SortType(Enum):
    """
    Enum class for sorting options.

    Attributes:
        BY_ITEM (int): Sort by item.
        BY_FREQ (int): Sort by frequency.
    """
    BY_ITEM = 0
    BY_FREQ = 1


class InvalidSortTypeError(Exception):
    """
    Custom exception class for invalid sorting type.

    Args:
        message (str): The error message.
    """

    def __init__(self, message):
        super().__init__(message)


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
    """
    Abstract base class representing a Frequency Table for analyzing and manipulating data frequencies.

    This class defines a common interface for working with frequency data, including methods for calculating
    statistics, filtering, mapping, and more.
    """

    def __init__(self, data=None):
        """
        Initialize a FrequencyTable.

        :param data: Optional initial data for creating the frequency table.
        """
        self._table = self._calculate_frequencies(data if data is not None else [])

    @abstractmethod
    def _calculate_frequencies(self, data):
        """
        Abstract method for calculating frequencies of data elements.

        :param data: The data to calculate frequencies for.
        :return: A frequency table (dictionary) where keys are elements and values are their frequencies.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Abstract method to represent the FrequencyTable as a string.

        :return: A string representation of the FrequencyTable.
        """
        pass

    @abstractmethod
    def mean(self):
        """
        Abstract method to calculate the mean (average) of the data.

        :return: The mean of the data.
        """
        pass

    @abstractmethod
    def median(self):
        """
        Abstract method to calculate the median of the data.

        :return: The median of the data.
        """
        pass

    @abstractmethod
    def mode(self):
        """
        Abstract method to calculate the mode of the data.

        :return: The mode of the data.
        """
        pass

    def __len__(self):
        """
        Get the number of unique elements in the FrequencyTable.

        :return: The number of unique elements.
        """
        return len(self._table.keys())

    def empty(self):
        """
        Check if the FrequencyTable is empty.

        :return: True if the FrequencyTable is empty, False otherwise.
        """
        return 0 == len(self)

    def display_table(self):
        """Print the string representation of the FrequencyTable."""
        print(self.__str__())

    def to_dict(self):
        """
        Convert the FrequencyTable to a dictionary.

        :return: A dictionary representation of the FrequencyTable.
        """
        return self._table.copy()

    def get_data(self):
        """
        Get a list of unique data elements in the FrequencyTable.

        :return: A list of unique data elements.
        """
        return self._table.keys()

    def get_frequencies(self):
        """
        Get a list of frequencies corresponding to data elements.

        :return: A list of frequencies.
        """
        return self._table.values()

    def get_total(self):
        """
        Get the total frequency count of all data elements.

        :return: The total frequency count.
        """
        return sum(self._table.values())

    def sort(self, by=SortType.BY_FREQ, acs=True):
        """
        Sort the FrequencyTable based on frequency or item, in ascending or descending order.

        :param by: Sort by frequency or item (SortType.BY_FREQ or SortType.BY_ITEM).
        :param acs: True for ascending, False for descending.
        :raises InvalidSortTypeError: If an invalid sorting type is specified.

        Example:
        >>> freq_table.sort(by=SortType.BY_FREQ, acs=False)
        """
        if not isinstance(by, SortType):
            raise InvalidSortTypeError(
                "Invalid SortType selected. `by` must be either SortType.BY_FREQ or SortType.BY_ITEM.")
        try:
            self._table = dict(sorted(self._table.items(), key=lambda item: item[by.value], reverse=not acs))
        except Exception as e:
            print(f"An error occurred while sorting: {e}")

    def append(self, data_to_append: Iterable):
        """
        Append data to the FrequencyTable and update frequencies.

        :param data_to_append: Data to append (an iterable, e.g., list, tuple).
        :raises TypeError: If the data_to_append is not an iterable.

        Example:
        >>> freq_table.append([1, 2, 2, 3])
        """
        if not isinstance(data_to_append, Iterable):
            raise TypeError("Invalid data type for `data_to_append`. It must be an iterable (e.g., list, tuple).")

        counter = collections.Counter(data_to_append)
        for item in counter:
            if item in self._table:
                self._table[item] += counter[item]
            else:
                if not isinstance(item, Hashable):
                    print(f"Warning: Skipping non-hashable item: {item}")
                else:
                    self._table[item] = counter[item]

    def merge(self, freqtable: 'FrequencyTable'):
        """
        Merge another FrequencyTable into this FrequencyTable.

        :param freqtable: Another FrequencyTable to merge.
        :raises TypeError: If freqtable is not a FrequencyTable.

        Example:
        >>> freq_table.merge(other_freq_table)
        """
        if not isinstance(freqtable, FrequencyTable):
            raise TypeError("Invalid data type for `freqtable`. It must be a FrequencyTable.")

        for item, freq in freqtable._table.items():
            if self._table.get(item) is None:
                self._table[item] = freq
            else:
                self._table[item] += freq

    def filter_by_freq(self, min_frequency: int, max_frequency: int):
        """
        Create a new FrequencyTable containing elements with frequencies within a specified range.

        :param min_frequency: Minimum frequency (inclusive).
        :param max_frequency: Maximum frequency (inclusive).
        :return: A new FrequencyTable containing filtered elements.
        """
        freqrange = range(min_frequency, max_frequency + 1)
        freqtable = self.__class__()

        for item, freq in self._table.items():
            if freq in freqrange:
                freqtable._table[item] = freq

        return freqtable

    def filter_by_class(self, predicate: Callable[[Any, Any], bool]):
        """
        Create a new FrequencyTable by applying a predicate function to filter elements.

        :param predicate: A callable function that takes (item, frequency) as arguments and returns a boolean.
        :return: A new FrequencyTable containing filtered elements.
        :raises TypeError: If the predicate function is not callable.

        Example:
        >>> def custom_predicate(item, freq):
        >>>     return freq > 3
        >>> filtered_freq_table = freq_table.filter_by_class(custom_predicate)
        """
        if not callable(predicate):
            raise TypeError("Invalid predicate function. It must be a callable function.")

        freqtable = self.__class__()
        for item, freq in self._table.items():
            try:
                if predicate(item, freq):
                    freqtable.append([item] * freq)
            except Exception as e:
                print(f"An error occurred while applying the predicate function: {e}")

        return freqtable

    def get_subset(self, subset_elements: Iterable):
        """
        Get a subset of the FrequencyTable containing specified elements.

        :param subset_elements: Elements to include in the subset (an iterable, e.g., list, tuple).
        :return: A new FrequencyTable containing the specified elements.

        Example:
        >>> subset = freq_table.get_subset([1, 2, 3])
        """

        if not isinstance(subset_elements, Iterable):
            raise TypeError("Invalid data type for `subset_elements`. It must be an iterable (e.g., list, tuple).")

        freqtable = self.__class__()
        for element in subset_elements:
            freq = self._table.get(element)
            if freq is not None:
                freqtable._table[element] = freq

        return freqtable

    def get_top_n_elements(self, n: int):
        """
        Get the top N elements with the highest frequencies.

        :param n: Number of top elements to retrieve.
        :return: A new FrequencyTable containing the top N elements.
        """

        if n <= 0:
            raise ValueError("Invalid value for `n`. It must be greater than 0.")

        freqtable = self.__class__()
        top_n_elements = heapq.nlargest(n, self._table.items(), lambda item: item[1])

        for item, freq in top_n_elements:
            freqtable._table[item] = freq

        return freqtable

    def get_lowest_n_elements(self, n: int):
        """
        Get the lowest N elements with the lowest frequencies.

        :param n: Number of lowest elements to retrieve.
        :return: A new FrequencyTable containing the lowest N elements.
        """

        if n <= 0:
            raise ValueError("Invalid value for `n`. It must be greater than 0.")

        freqtable = self.__class__()
        lowest_n_elements = heapq.nsmallest(n, self._table.items(), lambda item: item[1])

        for item, freq in lowest_n_elements:
            freqtable._table[item] = freq

        return freqtable

    def map_elements(self, func: Callable[[Any], Any]):
        """
        Apply a mapping function to elements in the FrequencyTable.

        :param func: A callable function that takes an element as input and returns a new element.
        :return: None

        Example:
        >>> def mapping_function(item):
        >>>     return item + 10
        >>> freq_table.map_elements(mapping_function)
        """

        if not callable(func):
            raise TypeError("Invalid mapping function. It must be a callable function.")

        items = list(self._table.keys())
        for item in items:
            try:
                new_item = func(item)
                freq = self._table[item]
                self._table.pop(item)
                if self._table.get(new_item) is not None:
                    self._table[new_item] += freq
                else:
                    self._table[new_item] = freq
            except Exception as e:
                print(f"An error occurred while mapping elements: {e}")

    def apply_frequency_operation(self, func: Callable[[Any], Any]):
        """
        Apply a frequency operation function to frequencies in the FrequencyTable.

        :param func: A callable function that takes a frequency as input and returns a new frequency.
        :return: None

        Example:
        >>> def frequency_operation(freq):
        >>>     return freq * 2
        >>> freq_table.apply_frequency_operation(frequency_operation)
        """

        if not callable(func):
            raise TypeError("Invalid mapping function. It must be a callable function.")

        items_with_neg_freq = []
        for item, freq in self._table.items():
            newfreq = func(freq)
            try:
                if newfreq <= 0:
                    raise ValueError(f"Warning: {item} deleted since its new frequency, {newfreq} <= 0")
            except ValueError as e:
                print(e)
                items_with_neg_freq.append(item)
            else:
                self._table[item] = newfreq

        for item in items_with_neg_freq:
            self._table.pop(item)

    def generate_random_data(self, sample_size: int):
        """
        Generate random data based on the frequencies in the FrequencyTable.

        :param sample_size: The number of random data points to generate.
        :return: A new FrequencyTable containing randomly generated data points.

        """

        if sample_size <= 0:
            raise ValueError("Sample size must be greater than zero.")

        if len(self) == 0:
            raise ValueError("Frequency table is empty. Cannot generate random data from an empty FrequencyTable.")

        items = list(self.get_data())
        relative_freqs = [freq / self.get_total() for freq in self.get_frequencies()]

        commutative_rfreqs = [relative_freqs[0]]

        for i in range(1, len(relative_freqs)):
            commutative_rfreqs.append(commutative_rfreqs[-1] + relative_freqs[i])

        freqt = self.__class__()
        for i in range(sample_size):
            try:
                rand = random()
                element_index = bisect_left(commutative_rfreqs, rand)
                if element_index < 0:
                    raise ValueError("Error in generating random data.")
                freqt.append([items[element_index]])
            except (ValueError, IndexError):
                print("An error occurred while generating random data. Retry or check input data.")

        return freqt


class DiscreteFrequencyTable(FrequencyTable):
    """
    Subclass of FrequencyTable representing a Discrete Frequency Table for analyzing and manipulating data frequencies.

    Usage:
        You can create an instance of DiscreteFrequencyTable and use it to analyze and manipulate discrete frequency data.

    Example:
        discrete_freq_table = DiscreteFrequencyTable(data=[1, 2, 2, 3])
    """

    def __init__(self, data=None):
        super().__init__(data)

    def _calculate_frequencies(self, data: Iterable):
        """
        Calculate frequencies of discrete data elements.

        :param data: The data to calculate frequencies for (an iterable, e.g., list, tuple).
        :return: A frequency table (dictionary) where keys are elements and values are their frequencies.
        """
        if not isinstance(data, Iterable):
            raise TypeError("Invalid data type for `data`. It must be an iterable (e.g., list, tuple).")

        counter = collections.Counter(data)
        return dict(counter.items())

    def __str__(self):
        """
        Generate a string representation of the DiscreteFrequencyTable.

        :return: A formatted string representing the frequency table.
        """
        max_len = 0

        for class_item in self._table:
            max_len = max(max_len, len(str(class_item)))

        max_len += 7

        table = ""
        table = table + f"{'Class':<{max_len}}" + "Frequency"

        for class_item in self._table:
            table = table + f"\n{class_item:<{max_len}}" + str(self._table[class_item])

        return table

    def mean(self):
        """
        Calculate the mean (average) of the discrete data.

        :return: The mean of the data.
        :raises ValueError: If the frequency table is empty.
        """
        if len(self) == 0:
            raise ValueError("Cannot calculate mean for an empty frequency table.")

        sum = 0
        for item, freq in self._table.items():
            sum += item * freq

        return sum / self.get_total()

    def median(self):
        """
        Calculate the median of the discrete data.

        :return: The median of the data.
        :raises ValueError: If the frequency table is empty.
        """
        if len(self) == 0:
            raise ValueError("Cannot calculate median for an empty frequency table.")

        items = []
        for item, freq in self._table.items():
            items.extend([item] * freq)

        items.sort()

        return items[int(self.get_total() / 2)] if self.get_total() % 2 == 1 else (
                (items[int(self.get_total() / 2)] + items[int(self.get_total() / 2) - 1]) / 2)

    def mode(self):
        """
        Calculate the mode of the discrete data.

        :return: The mode of the data.
        :raises ValueError: If the frequency table is empty.
        """
        if len(self) == 0:
            raise ValueError("Cannot calculate mode for an empty frequency table.")
        return list(self.get_top_n_elements(1).get_data())[0]

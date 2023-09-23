import json
from collections import Counter
from math import ceil
from bisect import bisect


def intfrequency_table(iterable: list[int]):
    """
    Computes the frequency table for integer values in the given iterable.

    Args:
        iterable (iterable of int): The input iterable containing integer values.

    Returns:
        tuple: A tuple containing two elements. The first element is a set of unique
               integers in the iterable, and the second element is a list of non-zero
               frequencies corresponding to each unique integer.

    Raises:
        ValueError: If the input iterable is empty or contains non-integer values.
    """
    if not iterable:
        raise ValueError("Input iterable is empty")

    if not all(isinstance(item, int) for item in iterable):
        raise ValueError("Input iterable must contain only integer values")

    min_val, max_val = min(iterable), max(iterable)
    freq = [0] * (max_val - min_val + 1)

    for item in iterable:
        freq[item - min_val] += 1

    non_zero_freq = [f for f in freq if f > 0]
    table = dict(zip(set(iterable), non_zero_freq))
    table["freqsum"] = sum(non_zero_freq)
    return table


def frequency_table(iterable: list):
    """
    Computes the frequency table for items in the given iterable.

    Args:
        iterable: The input iterable.

    Returns:
        list: A list of tuples, where each tuple contains an item from the iterable
              and its corresponding frequency in the iterable.

    Raises:
        ValueError: If the input iterable is empty.
    """
    if not iterable:
        raise ValueError("Input iterable is empty")

    counter = Counter(iterable)
    table = dict(counter.items())
    table["freqsum"] = sum(counter.values())
    return table


def class_frequency_table(iterable, num_classes=None, cut_points=None):
    """
    Computes a class frequency table for numeric values in the given iterable.

    Args:
        iterable: The input iterable containing numeric values.
        num_classes (int, optional): The number of classes to divide the data into.
        cut_points (list of float, optional): List of cut points for defining custom
            class intervals.

    Returns:
        dict: A dictionary where keys are class intervals (as ranges) and values
              are dictionaries containing the 'freq' (frequency) of values within
              each class interval. The table also includes a 'freqsum' representing
              the total frequency of all values.

    Raises:
        ValueError: If the input iterable is empty or invalid cut_points are provided.
    """
    assert num_classes is None or cut_points is None

    if not iterable:
        raise ValueError("Input iterable is empty")

    if cut_points is not None and (len(cut_points) < 2 or cut_points != sorted(cut_points)):
        raise ValueError("Invalid cut_points. It must be a list of at least two sorted values.")

    for item in iterable:
        if not isinstance(item, int) and not isinstance(item, float):
            raise ValueError("Input iterable is must to be a number.")

    if num_classes is None:
        num_classes = ceil(len(iterable) ** 0.5)

    min_val, max_val = min(iterable), max(iterable)
    range_size = ceil((max_val - min_val) / num_classes)

    table = {}

    if cut_points is None:
        for i in range(1, num_classes + 1):
            lower_bound = min_val + (i - 1) * range_size
            table[range(lower_bound, lower_bound + range_size)] = {}
    else:
        if min_val < cut_points[0]:
            cut_points.insert(0, min_val)
        if max_val > cut_points[-1]:
            cut_points.append(max_val)

        cut_points[-1] += 1

        for i in range(len(cut_points) - 1):
            table[range(cut_points[i], cut_points[i + 1])] = {}

    counter = Counter(iterable)
    items = sorted(counter.items())

    keys = sorted(counter.keys())

    cumulative_sums = [items[0][1]]

    for _, freq in items[1:]:
        cumulative_sums.append(cumulative_sums[-1] + freq)

    temp = 0
    fsum = 0

    for class_range in table:
        cs_for_current_class = cumulative_sums[bisect(keys, class_range.stop - 1) - 1]
        table[class_range]["freq"] = cs_for_current_class - temp
        fsum += cs_for_current_class - temp
        temp = cs_for_current_class

    table['freqsum'] = fsum
    return table


def relative_frequency_table(iterable, num_classes=None, cut_points=None):
    """
    Computes a relative frequency table for numeric values in the given iterable.

    Args:
        iterable: The input iterable containing numeric values.
        num_classes (int, optional): The number of classes to divide the data into.
        cut_points (list of float, optional): List of cut points for defining custom
            class intervals.

    Returns:
        dict: A dictionary where keys are class intervals (as ranges) and values
              are dictionaries containing the 'rfreq' (relative frequency) of values
              within each class interval. The table also includes an 'rfreqsum'
              representing the total relative frequency of all values.

    Raises:
        ValueError: If the input iterable is empty or invalid cut_points are provided.
    """
    if not iterable:
        raise ValueError("Input iterable is empty")

    if cut_points is not None and (len(cut_points) < 2 or cut_points != sorted(cut_points)):
        raise ValueError("Invalid cut_points. It must be a list of at least two sorted values.")

    table = class_frequency_table(iterable, num_classes, cut_points)
    table["rfreqsum"] = 0
    for _class in table:
        if isinstance(_class, range):
            _class_rfreq = table[_class]["freq"] / table["freqsum"]
            table[_class]["rfreq"] = _class_rfreq
            table["rfreqsum"] += _class_rfreq
    return table


def cumulative_frequency_table(iterable, num_classes=None, cut_points=None):
    """
    Computes a cumulative frequency table for numeric values in the given iterable.

    Args:
        iterable: The input iterable containing numeric values.
        num_classes (int, optional): The number of classes to divide the data into.
        cut_points (list of float, optional): List of cut points for defining custom
            class intervals.

    Returns:
        dict: A dictionary where keys are class intervals (as ranges) and values
              are dictionaries containing the 'cfreq' (cumulative frequency) of values
              within each class interval.

    Raises:
        ValueError: If the input iterable is empty or invalid cut_points are provided.
    """
    if not iterable:
        raise ValueError("Input iterable is empty")

    if cut_points is not None and (len(cut_points) < 2 or cut_points != sorted(cut_points)):
        raise ValueError("Invalid cut_points. It must be a list of at least two sorted values.")

    table = class_frequency_table(iterable, num_classes, cut_points)
    temp = 0
    for _class in table:
        if isinstance(_class, range):
            table[_class]["cfreq"] = table[_class]["freq"] + temp
            temp = table[_class]["cfreq"]
    return table


def jsonify(table, file_path):
    """
    Serialize a dictionary to JSON format and write it to a file.

    Args:
        table (dict): The dictionary to be serialized to JSON.
        file_path (str): The path to the JSON file where the data will be written.

    Raises:
        IOError: If there is an issue with writing to the file.
    """
    table_copy = {}
    for key, value in table.items():
        if isinstance(key, range):
            key = f'{key.start}-{key.stop}'
        table_copy[key] = value

    try:
        with open(file_path, 'w') as output:
            json.dump(table_copy, output, indent=4)
    except IOError as e:
        print(f"Error writing to file: {e}")

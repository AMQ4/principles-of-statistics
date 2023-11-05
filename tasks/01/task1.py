from collections import Counter
from typing import Iterable, Union
import math


def mean(l: Iterable[Union[int, float]]) -> float:
    """
    Calculate the mean (average) of a list of numbers.

    Args:
        l (Iterable[Union[int, float]]): List of numbers.

    Returns:
        float: The mean of the input list.
    """
    return sum(l) / len(l)


def percentile(l: Iterable[Union[int, float]], p):
    """
    Calculate the p-th percentile of a list of numbers.

    Args:
        l (Iterable[Union[int, float]]): List of numbers.
        p (float): The percentile value (0.0 to 1.0).

    Returns:
        float: The p-th percentile of the input list.
    """
    p *= len(l)
    if p.is_integer():
        return (l[int(p)] + l[int(p) - 1]) / 2
    else:
        return l[math.floor(p)]


def S(l: Iterable[Union[int, float]]):
    """
    Calculate the sample variance (S) of a list of numbers.

    Args:
        l (Iterable[Union[int, float]]): List of numbers.

    Returns:
        float: The sample variance of the input list.
    """
    x = mean(l)
    squared_diff_sum = sum((i - x) ** 2 for i in l)
    return squared_diff_sum / (len(l) - 1)


with open("01data") as data:
    try:
        arr = list(map(int, data.readline().split()))
        arr.sort()
    except Exception as e:
        print(e)

counter = Counter(arr)
mode = counter.most_common(1)
x = mean(arr)
median = percentile(arr, 0.5)
var = S(arr)

print(f"Sample Mean: {x}")
print(f"Sample Mode: {'∅' if mode == 1 and len(arr) > 1 else mode[0][0]}")
print(f"Sample Median: {median}")
print(f"Sample's 73rd percentile: {percentile(arr, 73 / 100)}")
print(f"Sample's 20th percentile: {percentile(arr, 20 / 100)}")
print(f"Sample variance: {var:.2f}")
print(f"Population standard deviation: {var * (len(arr) - 1) / len(arr):.2f}")
print(f"Sample IQR: {percentile(arr, 0.75) - percentile(arr, 0.25)}")

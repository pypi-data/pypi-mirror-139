"""
Produce an optimal partition by solving an integer linear program (ILP).

Programmer: Erel Segal-Halevi
Since: 2022-02

Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576
"""

from typing import List, Callable, Any
from numbers import Number
from prtpy import objectives as obj, outputtypes as out
from math import inf

import mip


def optimal(
    numbins: int,
    items: List[Any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    outputtype: out.OutputType = out.Partition,
    copies=1,
    max_seconds=inf,
):
    """
    Produce a partition that minimizes the given objective,
    by solving an integer linear program (ILP).

    Parameters
    ----------
    copies
        how many copies are there from each number.
        Can be either a single integer (the same #copies for all numbers),
        or a dict mapping an item to the number of copies of that item.
        Default: 1


    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> optimal(3, walter_numbers, objective=obj.MinimizeDifference, outputtype=out.PartitionAndSums).sort()
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> optimal(3, walter_numbers, objective=obj.MinimizeLargestSum, outputtype=out.PartitionAndSums).sort()
    Bin #0: [27, 26], sum=53.0
    Bin #1: [46, 16], sum=62.0
    Bin #2: [39, 13, 10], sum=62.0
    >>> optimal(3, walter_numbers, objective=obj.MaximizeSmallestSum, outputtype=out.PartitionAndSums).sort()
    Bin #0: [46, 10], sum=56.0
    Bin #1: [27, 16, 13], sum=56.0
    Bin #2: [39, 26], sum=65.0
    >>> optimal(3, walter_numbers, objective=obj.MaximizeSmallestSum, outputtype=out.SmallestSum)
    56.0

    >>> from prtpy.partitioning import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['a', 'g'], ['c', 'd', 'e'], ['b', 'f']]
    >>> partition(algorithm=optimal, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])
    """

    ibins = range(numbins)
    if isinstance(copies, Number):
        copies = {item: copies for item in items}

    model = mip.Model("partition")
    counts: dict = {
        item: [model.add_var(var_type=mip.INTEGER) for ibin in ibins] for item in items
    }  # counts[i][j] determines how many times item i appears in bin j.
    bin_sums = [
        sum([counts[item][ibin] * map_item_to_value(item) for item in items]) for ibin in ibins
    ]

    model.objective = mip.minimize(
        objective.get_value_to_minimize(bin_sums, are_sums_in_ascending_order=True)        
    )

    # Construct the list of constraints:
    counts_are_non_negative = [counts[item][ibin] >= 0 for ibin in ibins for item in items]
    each_item_in_one_bin = [
        sum([counts[item][ibin] for ibin in ibins]) == copies[item] for item in items
    ]
    bin_sums_in_ascending_order = [  # a symmetry-breaker
        bin_sums[ibin + 1] >= bin_sums[ibin] for ibin in range(numbins - 1)
    ]
    constraints = counts_are_non_negative + each_item_in_one_bin + bin_sums_in_ascending_order
    for constraint in constraints: model += constraint

    # Solve the ILP:
    model.verbose = 0
    status = model.optimize(max_seconds=max_seconds)
    if status != mip.OptimizationStatus.OPTIMAL:
        raise ValueError(f"Problem status is not optimal - it is {status}.")

    # Construct the output:
    bins = outputtype.create_empty_bins(numbins)
    for ibin in ibins:
        for item in items:
            count_item_in_bin = int(counts[item][ibin].x)
            for _ in range(count_item_in_bin):
                bins.add_item_to_bin(item, map_item_to_value(item), ibin, inplace=True)
    return outputtype.extract_output_from_bins(bins)


if __name__ == "__main__":
    import doctest, logging

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

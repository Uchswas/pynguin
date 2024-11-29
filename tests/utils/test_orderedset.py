#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2024 Pynguin Contributors
#
#  SPDX-License-Identifier: MIT
#
import copy

import pytest
import pandas as pd

from pynguin.utils.orderedset import OrderedSet


# @pytest.mark.parametrize("length, iterable", [(0, []), (3, [1, 2, 3]), (2, [1, 2, 2])])
# def test_orderedset_len(length, iterable):
#     assert len(OrderedSet(iterable)) == length
@pytest.mark.parametrize(
    "length, iterable",
    [
        (0, []),
        (3, [1, 2, 3]),
        (2, [1, 2, 2]),
        (1, [pd.DataFrame({"col1": [1, 2]})]),  # Adding DataFrame
    ],
)
def test_orderedset_len(length, iterable):
    assert len(OrderedSet(iterable)) == length


def test_orderedset_copy():
    ordered = OrderedSet([1, 2, 3])
    copied = copy.copy(ordered)
    assert ordered == copied


# @pytest.mark.parametrize("element, result", [(0, False), (3, True)])
# def test_orderedset_contains(element, result):
#     assert (element in OrderedSet([1, 2, 3])) == result


@pytest.mark.parametrize(
    "element, result",
    [
        (0, False),
        (3, True),
        (pd.DataFrame({"col1": [1, 2]}), True),  # DataFrame that exists in the set
        (pd.DataFrame({"col1": [3, 4]}), False),  # DataFrame that does not exist
    ],
)
def test_orderedset_contains(element, result):
    df = pd.DataFrame({"col1": [1, 2]})
    ordered_set = OrderedSet([1, 2, 3, df])
    assert (element in ordered_set) == result


def test_orderedset_reversed():
    ordered = OrderedSet([1, 2, 3])
    assert tuple(reversed(ordered)) == (3, 2, 1)


@pytest.mark.parametrize(
    "first,second,result",
    [
        ([1, 2, 3], [1, 2, 3], True),
        ([1, 2, 3], [1, 2], False),
        ([1, 2, None], [1, 2], False),
        ([1, 2, 3], [1, 3, 2], False),
    ],
)
def test_orderedset_eq(first, second, result):
    assert (OrderedSet(first) == OrderedSet(second)) == result


@pytest.mark.parametrize(
    "first, second, result",
    [([], [], []), ([1], [], [1]), ([], [1], [1]), ([1], [2], [1, 2])],
)
def test_ordereset_or_union(first, second, result):
    assert OrderedSet(first) | OrderedSet(second) == OrderedSet(result)
    assert OrderedSet(first).union(OrderedSet(second)) == OrderedSet(result)


@pytest.mark.parametrize(
    "first, second, result",
    [([], [], []), ([1], [], []), ([], [1], []), ([1], [2], []), ([1, 2], [2, 3], [2])],
)
def test_ordereset_and_intersection(first, second, result):
    assert OrderedSet(first) & OrderedSet(second) == OrderedSet(result)
    assert OrderedSet(first).intersection(OrderedSet(second)) == OrderedSet(result)

def test_orderedset_union_with_dataframe():
    df1 = pd.DataFrame({"col1": [1, 2]})
    df2 = pd.DataFrame({"col2": [3, 4]})
    set1 = OrderedSet([1, df1])
    set2 = OrderedSet([df2, 2])
    result = set1 | set2
    assert len(result) == 4
    assert df1 in result
    assert df2 in result


def test_orderedset_intersection_with_dataframe():
    df1 = pd.DataFrame({"col1": [1, 2]})
    df2 = pd.DataFrame({"col2": [3, 4]})
    set1 = OrderedSet([1, df1])
    set2 = OrderedSet([df1, df2])
    result = set1 & set2
    assert len(result) == 1
    assert df1 in result
    assert df2 not in result


def test_orderedset_reversed_with_dataframe():
    df = pd.DataFrame({"col1": [1, 2]})
    ordered_set = OrderedSet([1, df, 3])
    assert tuple(reversed(ordered_set)) == (3, df, 1)


def test_orderedset_eq_with_dataframe():
    df1 = pd.DataFrame({"col1": [1, 2]})
    df2 = pd.DataFrame({"col1": [1, 2]})
    set1 = OrderedSet([1, df1])
    set2 = OrderedSet([1, df2])
    assert set1 != set2  # Different DataFrame instances
    assert OrderedSet([df1]) == OrderedSet([df1])  # Same instance


def test_orderedset_copy_with_dataframe():
    df = pd.DataFrame({"col1": [1, 2]})
    ordered = OrderedSet([1, df, 3])
    copied = copy.copy(ordered)
    assert ordered == copied
    assert df in copied

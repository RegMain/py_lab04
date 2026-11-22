
from queue import Empty

from py_lab04.sort import insertion_sort, quick_sort
from py_lab04.data_generator import DataGenerator
from py_lab04.queue import Queue, EmptyQueueError

import pytest

@pytest.mark.parametrize(
    "data", [
        ([]),
        ([1]),
        ([1,2,3,4,5,6,7,8]),
        ([8,7,6,5,4,3,2,1]),
        ([1,2,2,5,1,1,8,3,3,1,1,3,7,8]),
        ([-1,-2,-3,-4,-5,-6,-7])
    ]
)
def test_insertion_sort(data):
    data_copy = data.copy()
    insertion_sort(data_copy)
    assert sorted(data) == data_copy

@pytest.mark.parametrize(
    "data", [
        ([]),
        ([1]),
        ([1,2,3,4,5,6,7,8]),
        ([8,7,6,5,4,3,2,1]),
        ([1,2,2,5,1,1,8,3,3,1,1,3,7,8]),
        ([-1,-2,-3,-4,-5,-6,-7])
    ]
)
def test_quick_sort(data):
    data_copy = data.copy()
    quick_sort(data_copy)
    assert sorted(data) == data_copy

def test_generator_seed():
    for i in range(5):
        generator_1 = DataGenerator(i)
        generator_2 = DataGenerator(i)
        assert generator_1.get_random_data(20, int) == generator_2.get_random_data(20, int)

def test_empty_queue_error():
    with pytest.raises(EmptyQueueError):
        q = Queue()
        q.pop()

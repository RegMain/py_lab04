
from typing import Callable

def insertion_sort(values: list, key: Callable | None = None, reverse: bool = False) -> None:
    if not isinstance(values, list):
        raise TypeError(
            f"Expected {list}, got {type(values)} instead.\n"
        )
    if key is not None and not callable(key):
        raise TypeError(
            f"Expected None or function, got {type(key)} instead.\n"
        )

    if key is None:
        values_with_key = [(x, x) for x in values]
    else:
        values_with_key = [(key(x), x) for x in values]

    for i in range(1, len(values)):
        for j in range(i, 0, -1):
            condition: bool = values_with_key[j][0] < values_with_key[j - 1][0]
            condition = not condition if reverse else condition
            if condition:
                values_with_key[j], values_with_key[j - 1] = values_with_key[j - 1], values_with_key[j]

    for i in range(len(values)):
        values[i] = values_with_key[i][1]

def heap_sort(values: list, key: Callable | None = None, reverse: bool = False) -> None:
    if not isinstance(values, list):
        raise TypeError(
            f"Expected {list}, got {type(values)} instead.\n"
        )
    if key is not None and not callable(key):
        raise TypeError(
            f"Expected None or function, got {type(key)} instead.\n"
        )

    if key is None:
        values_with_key = [(x, x) for x in values]
    else:
        values_with_key = [(key(x), x) for x in values]

    def heap_condition(first, second) -> bool:
        if reverse:
            return first[0] > second[0]
        else:
            return first[0] < second[0]

    def make_heap(heap: list, size: int, i: int) -> None:
        root: int = i
        left: int = 2 * i + 1
        right: int = 2 * i + 2
        if left < size and heap_condition(heap[root], heap[right]):
            root = left
        if right < size and heap_condition(heap[root], heap[right]):
            root = right
        if root != i:
            heap[i], heap[root] = heap[root], heap[i]
            make_heap(heap, size, root)

    size: int = len(values)
    for i in range(size, -1, -1):
        make_heap(values_with_key, size, i)
    for i in range(size):
        values[size - i - 1] = values_with_key[0][1]
        values_with_key[0] = values_with_key[size - i - 1]
        make_heap(values_with_key, size - i, 0)

def quick_sort(values: list, key: Callable | None = None, reverse: bool = False) -> None:
    if not isinstance(values, list):
        raise TypeError(
            f"Expected {list}, got {type(values)} instead.\n"
        )
    if key is not None and not callable(key):
        raise TypeError(
            f"Expected None or function, got {type(key)} instead.\n"
        )

    if key is None:
        values_with_key = [(x, x) for x in values]
    else:
        values_with_key = [(key(x), x) for x in values]

    def sort_condition(first, second) -> bool:
        if reverse:
            return first[0] > second[0]
        else:
            return first[0] < second[0]

    def sort_itself(begin: int, end: int) -> None:
        if begin >= end:
            return
        nonlocal values_with_key
        pivot: tuple
        medium: int = (begin + end) // 2
        variants: list = [begin, medium, end]
        variants = [min(variants, key=lambda x: values_with_key[x][0]), sum(variants), max(variants, key=lambda x: values_with_key[x][0])]
        variants[1] -= (variants[0] + variants[2])
        values_with_key[variants[1]], values_with_key[medium] = values_with_key[medium], values_with_key[variants[1]]
        pivot = values_with_key[medium]
        lower_iter: int = begin
        higher_iter: int = end
        while True:
            while sort_condition(values_with_key[lower_iter], pivot):
                lower_iter += 1
            while sort_condition(pivot, values_with_key[higher_iter]):
                higher_iter -= 1
            if lower_iter >= higher_iter:
                break
            values_with_key[lower_iter], values_with_key[higher_iter] = values_with_key[higher_iter], values_with_key[lower_iter]
        sort_itself(begin, higher_iter)
        sort_itself(higher_iter + 1, end)

    sort_itself(0, len(values) - 1)

    for i in range(len(values)):
        values[i] = values_with_key[i][1]


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
        values_with_key = [x for x in values]
    else:
        values_with_key = [(key(x), x) for x in values]

    for i in range(1, len(values)):
        for j in range(i, 0, -1):
            condition: bool = values_with_key[j] < values_with_key[j - 1]
            condition = not condition if reverse else condition
            if condition:
                values_with_key[j], values_with_key[j - 1] = values_with_key[j - 1], values_with_key[j]

    if key is None:
        for i in range(len(values)):
            values[i] = values_with_key[i]
    else:
        for i in range(len(values)):
            values[i] = values_with_key[i][1]

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
        values_with_key = [x for x in values]
    else:
        values_with_key = [(key(x), x) for x in values]

    def sort_condition(first, second) -> bool:
        if reverse:
            return first > second
        else:
            return first < second

    def sort_itself(begin: int, end: int) -> None:
        if begin >= end:
            return
        nonlocal values_with_key
        middle: int = (begin + end) // 2
        if values_with_key[begin] > values_with_key[middle]:
            values_with_key[begin], values_with_key[middle] = values_with_key[middle], values_with_key[begin]
        if values_with_key[begin] > values_with_key[end]:
            values_with_key[begin], values_with_key[end] = values_with_key[end], values_with_key[begin]
        if values_with_key[middle] > values_with_key[end]:
            values_with_key[middle], values_with_key[end] = values_with_key[end], values_with_key[middle]
        pivot: tuple = values_with_key[middle]
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
            lower_iter += 1
            higher_iter -= 1
        sort_itself(begin, higher_iter)
        sort_itself(higher_iter + 1, end)

    sort_itself(0, len(values) - 1)

    if key is None:
        for i in range(len(values)):
            values[i] = values_with_key[i]
    else:
        for i in range(len(values)):
            values[i] = values_with_key[i][1]

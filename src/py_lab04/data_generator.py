import random
import time
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class DataBounds:
    lower: int
    upper: int
    additional: list

    def check(self) -> None:
        if not isinstance(self.lower, int) or not isinstance(self.upper, int) \
            or not isinstance(self.additional ,list):
            raise TypeError(
                f"Expected {int}, {int}, {list} got {type(self.lower)}, {type(self.upper)}, {type(self.additional)} instead.\n"
            )
        for data in self.additional:
            if not isinstance(data, int):
                raise TypeError(
                    f"Expected self.additional elements to be {int} type, got {type(data)} instead.\n"
                )

    def __post_init__(self) -> None:
        self.check()

class DataGenerator:
    __rng: random.Random
    __seed: int
    __bounds: dict[type, DataBounds]

    def __init__(self, seed: int | None = None, bounds: dict[type, DataBounds] | None = None) -> None:
        if not isinstance(seed, int) and seed is not None:
            raise TypeError(
                f"Expected {int}, got {type(seed)} instead.\n"
            )
        if seed is not None:
            self.__seed = seed
        else:
            self.__seed = time.time_ns()
        self.__bounds = {
            int: DataBounds(-1_000_000_000, 1_000_000_000, []),
            float: DataBounds(-1_000_000_000, 1_000_000_000, []),
            str: DataBounds(1, 10000, [1, 30])
        }
        if bounds:
            if not isinstance(bounds, dict):
                raise TypeError(
                    f"Expected {dict}, got {type(bounds)} instead.\n"
                )
            if set(bounds.keys()) != set(self.__bounds.keys()):
                raise ValueError(
                    f"Bounds expected to have {self.__bounds.keys()} types, not {bounds.keys()}.\n"
                )
            for data_bounds in bounds:
                data_bounds.check()
        self.__rng = random.Random(self.__seed)

    def get_seed(self) -> int:
        return self.__seed

    def get_bounds(self) -> dict[type, DataBounds]:
        return deepcopy(self.__bounds)

    def set_seed(self, seed: int) -> None:
        if not isinstance(seed, int):
            raise TypeError(
                f"Expected {int}, got {type(seed)} instead.\n"
            )
        self.__seed = seed
        self.__rng.seed(self.__seed)

    def set_bounds(self, bounds: dict[type, DataBounds]):
        if not isinstance(bounds, dict):
            raise TypeError(
                f"Expected {dict}, got {type(bounds)} instead.\n"
            )
        if set(bounds.keys()) != set(self.__bounds.keys()):
            raise ValueError(
                f"Bounds expected to have {self.__bounds.keys()} types, not {bounds.keys()}.\n"
            )
        for data_bounds in bounds:
            data_bounds.check()
        self.__bounds = bounds

    def get_random_data(self, size: int, data_type: type) -> list:
        if not isinstance(size, int):
            raise TypeError(
                f"Expected {int} type size, got {type(size)} instead.\n"
            )
        if data_type not in self.__bounds:
            print(self.__bounds)
            raise TypeError(
                f"{data_type} is either not type or not supported.\n"
            )
        lower: int = self.__bounds[data_type].lower
        upper: int = self.__bounds[data_type].upper
        if data_type == int:
            return [self.__rng.randint(lower, upper) for _ in range(size)]
        elif data_type == float:
            return [
                self.__rng.random() * self.__rng.randint(lower, upper)
                for _ in range(size)
            ]
        else:
            word_len_lower: int = self.__bounds[str].additional[0]
            word_len_upper: int = self.__bounds[str].additional[1]
            return [
                "".join([
                    chr(self.__rng.randint(lower, upper)) for _ in range(word_len_lower, word_len_upper)
                ]) for _ in range(size)
            ]

    def get_sorted_data(self, size: int, data_type: type, key: Callable | None = None, reverse: bool = False) -> list:
        if not isinstance(key, Callable) and key is not None:
            raise TypeError(
                "Given key is not callable.\n"
            )
        return sorted(self.get_random_data(size, data_type), key=key, reverse=reverse)

    def get_reversed_data(self, size: int, data_type: type, key: Callable | None = None) -> list:
        return self.get_sorted_data(size, data_type, key, True)

    def get_almost_sorted_data(self, size: int, data_type: type, key: Callable | None = None) -> list:
        data: list = self.get_sorted_data(size, data_type, key)
        if size > 1:
            index: int = self.__rng.randint(1, size - 1)
            data[index - 1], data[index] = data[index], data[index - 1]
        return data

    def get_data_with_duplicates(self, size: int, data_type: type) -> list:
        if not isinstance(size, int):
            raise TypeError(
                f"Expected {int} type size, got {type(size)} instead.\n"
            )
        data: list = self.get_random_data(size // 2, data_type)
        data += data
        if (size % 2 == 1):
            data += data[0]
        self.__rng.shuffle(data)
        return data

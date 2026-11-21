from dataclasses import dataclass
import random
import time
from typing import Callable

@dataclass
class DataBounds:
    lower: int
    upper: int
    additional: list

class DataGenerator:
    __rng: random.Random
    __seed: int
    __bounds: dict[type, DataBounds]

    def __init__(self, seed: int | None = None, bounds: dict[type, DataBounds] | None = None) -> None:
        if not isinstance(seed, int):
            raise TypeError(
                f"Expected {int}, got {type(seed)} instead.\n"
            )
        if seed:
            self.__seed = seed
        else:
            self.__seed = time.time_ns()
        if bounds:
            self.__bounds = bounds
        else:
            self.__bounds = {
                int: DataBounds(-1_000_000_000, 1_000_000_000, []),
                float: DataBounds(-1_000_000_000, 1_000_000_000, []),
                str: DataBounds(1, 10000, [1, 30])
            }
        self.__rng = random.Random()
        self.__rng.seed(self.__seed)

    def get_seed(self) -> int:
        return self.__seed

    def get_random_data(self, size: int, data_type: type) -> list:
        if not isinstance(size, int):
            raise TypeError(
                f"Expected {int} type size, got {type(size)} instead.\n"
            )
        if not isinstance(data_type, type) or type not in self.__bounds:
            raise TypeError(
                f"{data_type} is either not type or not supported.\n"
            )
        lower: int = self.__bounds[type].lower
        upper: int = self.__bounds[type].upper
        if type == int:
            return [self.__rng.randint(lower, upper) for _ in range(size)]
        elif type == float:
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

    def get_sorted_data(self, size: int, data_type: type, key: Callable, reverse: bool = False) -> list:
        if not isinstance(key, Callable):
            raise TypeError(
                f"Given key is not callable.\n"
            )
        return sorted(self.get_random_data(size, data_type), key=key, reverse=reverse)

    def get_reversed_data(self, size: int, data_type: type, key: Callable) -> list:
        return self.get_sorted_data(size, data_type, key, True)

    def get_almost_sorted_data(self, size: int, data_type: type, key: Callable) -> list:
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

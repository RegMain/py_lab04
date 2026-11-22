import signal
import time
from collections.abc import Callable

from py_lab04.data_generator import DataBounds, DataGenerator
from py_lab04.sort import insertion_sort, quick_sort

NS_IN_S: int = 1_000_000_000

def is_sorted(data: list, reverse: bool = False) -> bool:
    for i in range(len(data) - 1):
        if reverse:
            if data[i + 1] < data[i]:
                return False
        else:
            if data[i] > data[i + 1]:
                return False
    return True

class UnsortedError(Exception):
    pass

class SortBenchmark:
    __generator: DataGenerator
    __tests: dict[str, Callable]
    __sort_function: Callable | None
    data_sizes: tuple = (10_000, 100_000, 1_000_000, 10_000_000)
    results: dict[str, dict[int, int]]
    max_time: int

    def __init__(self, seed: int | None = None, bounds: dict[type, DataBounds] | None = None,
        data_sizes: tuple | None = None, max_time: int = 30) -> None:
        self.__generator = DataGenerator(seed, bounds)
        if data_sizes is not None:
            self.data_sizes = data_sizes
        if not isinstance(max_time, int):
            raise TypeError(
                f"Expected max_time to be {int} type, got {type(max_time)} instead.\n"
            )
        self.max_time = max_time
        self.__tests = {
            "random_data": self.__generator.get_random_data,
            "sorted_data": self.__generator.get_sorted_data,
            "reversed_data": self.__generator.get_reversed_data,
            "almost_sorted_data": self.__generator.get_reversed_data,
            "duplicates_data": self.__generator.get_data_with_duplicates
        }
        self.results = {}
        self.__sort_function = None

    def get_seed(self) -> int:
        return self.__generator.get_seed()

    def __test_one(self, sort_function: Callable, iterations: int, test_name: str, gen_function: Callable) -> None:

        def timeout_handler(signum, frame):
            raise TimeoutError

        timeout_flag: bool = False
        for data_size in self.data_sizes:
            data = gen_function(data_size, int)
            if timeout_flag:
                self.results[test_name][data_size] = NS_IN_S * (self.max_time + 1)
                continue
            print(f"Dataset ({data_size}) for test {test_name} was created.")
            for i in range(iterations):
                data_i = data.copy()
                before = time.time_ns()
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(self.max_time)
                try:
                    sort_function(data_i)
                except TimeoutError:
                    self.results[test_name][data_size] = iterations * NS_IN_S * (self.max_time + 1)
                    timeout_flag = True
                finally:
                    signal.alarm(0)
                if timeout_flag:
                    break
                after = time.time_ns()
                if not is_sorted(data_i):
                    raise UnsortedError(
                        f"Data is not sorted after '{test_name}' test.\n"
                    )
                self.results[test_name][data_size] += after - before
                print("Test has succesfully ended")
            self.results[test_name][data_size] = round(self.results[test_name][data_size] / iterations)

    def test(self, sort_function: Callable, iterations: int = 5) -> None:
        self.results = {}
        for test_name in self.__tests:
            self.results[test_name] = {}
            for data_size in self.data_sizes:
                self.results[test_name][data_size] = 0
        if not isinstance(sort_function, Callable) or not isinstance(iterations, int):
            raise TypeError(
                f"Expected {Callable}, {int}, got {type(sort_function)}, {type(iterations)} instead.\n"
            )
        for test_name, gen_function in self.__tests.items():
            self.__test_one(sort_function, iterations, test_name, gen_function)
            print(f"Test {test_name} has completed.")
        self.__sort_function = sort_function

    def make_report(self, filename: str = "benchmark_report.md") -> None:
        if not self.__sort_function:
            return
        with open(filename, "w") as file:
            file.write(f"function: {self.__sort_function.__name__}\n")
            file.write(f"seed: {self.get_seed()}\n\n")
            file.write("| **Test** |")
            file.writelines(f" **Time ({size})** |" for size in self.data_sizes)
            file.write("\n")
            file.write("| --- |")
            file.writelines(" --- |" for _ in self.data_sizes)
            file.write("\n")
            for test_name in self.__tests:
                file.write(f"| *{test_name}* |")
                file.writelines(f" {value / NS_IN_S}s |" if value <= self.max_time * NS_IN_S else f" >{self.max_time}s |"
                    for value in self.results[test_name].values())
                file.write("\n")

if __name__ == "__main__":

    benchmark = SortBenchmark(max_time=60, seed=1795356677893634237)

    def python_sort(data):
        data.sort()

    benchmark.test(python_sort)
    benchmark.make_report("python.md")
    benchmark.test(insertion_sort)
    benchmark.make_report("insertion.md")
    benchmark.test(quick_sort)
    benchmark.make_report("quick.md")

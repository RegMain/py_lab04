
from typing import Any

class EmptyQueueError(Exception):
    pass

class Queue:
    __data: list
    __size: int
    __capacity: int
    __first: int

    def __init__(self) -> None:
        self.__data = []
        self.__size = 0
        self.__capacity = 0
        self.__first = 0

    def __len__(self) -> int:
        return self.__size

    def __bool__(self) -> bool:
        return not self.__size

    def push(self, value) -> None:
        if (self.__size < self.__capacity):
            self.__data[(self.__size + self.__first) % self.__capacity] = value
        else:
            self.__data.append(*[0 for _ in range(self.__capacity)])
            self.__size += 1
            for i in range(self.__first):
                self.__data[self.__capacity + i] = self.__data[i]
            self.__capacity *= 2

    def pop(self) -> Any:
        if not self.__data:
            raise EmptyQueueError(
                "Attempting to pop value from empty queue.\n"
            )
        self.__size -= 1
        self.__first += 1
        return self.__data[self.__first - 1]

    def front(self) -> Any:
        if not self.__data:
            raise EmptyQueueError(
                "Attempting to take value from empty queue.\n"
            )
        return self.__data[self.__first]

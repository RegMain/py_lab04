
from typing import Any


class EmptyQueueError(Exception):
    pass

class Queue:
    __data: list
    __size: int

    def __init__(self) -> None:
        self.__size = 0
        self.__data = []

    def __len__(self) -> int:
        return self.__size

    def __bool__(self) -> bool:
        return bool(self.__size)

    def push(self, value) -> None:
        self.__data.append(value)

    def pop(self) -> Any:
        if not self.__size:
            raise EmptyQueueError(
                "Attempting to pop value from empty queue.\n"
            )
        self.__size -= 1
        return self.__data.pop(0)

    def front(self) -> Any:
        if not self.__size:
            raise EmptyQueueError(
                "Attempting to take value from empty queue.\n"
            )
        return self.__data[0]

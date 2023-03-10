import sys


class Queue:

    def __init__(self, size):
        self.__array = [0 for _ in range(size)]
        self.__size = size
        self.__front = 0
        self.__rear = 0
        self.__count = 0

    def enqueue(self, obj):
        self.__array[self.__front] = obj
        self.__front = (self.__front + 1) % self.__size
        self.__count += 1

    def dequeue(self):
        item = self.__array[self.__rear]
        self.__rear = (self.__rear + 1) % self.__size
        self.__count -= 1
        return item

    def is_empty(self):
        return self.__count == 0


class Lock:

    def __init__(self, flags: list):
        self.__queue = Queue(len(flags))
        self.__flags = flags
        self.__turn = sys.maxsize

    def __is_free(self):
        return not any(self.__flags)

    def acquire(self, process_id) -> bool:
        if not self.__is_free():
            self.__queue.enqueue(process_id)
            return False
        self.__flags[process_id] = True
        return self.__flags[process_id]

    def release(self, process_id):
        self.__flags[process_id] = False
        if not self.__queue.is_empty():
            next_process = self.__queue.dequeue()
            self.__flags[next_process] = True


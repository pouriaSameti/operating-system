import sys


class Temp:

    def __init__(self):
        self.__value = [-sys.maxsize]

    def is_empty(self):
        return -sys.maxsize == self.__value

    def set(self, amount: float):
        self.__value = amount

    def get(self):
        if self.is_empty():
            raise Exception("Temp Register is Empty")

        return self.__value

    def reset(self):
        self.__value = -sys.maxsize

    def __str__(self):
        return f"Temp: {self.get()}"


class Accumulator:

    def __init__(self):
        self.__value = -sys.maxsize

    def reset(self):
        self.__value = -sys.maxsize

    def is_empty(self):
        return -sys.maxsize == self.__value

    def set_to_temp(self, temp: Temp):
        if temp.is_empty():
            raise Exception("Temp Register is Null.We can't Write into Accumulator")
        self.__value = temp.get()

    def set(self, value: float):
        self.__value = value

    def get(self):
        if self.is_empty():
            raise Exception("Accumulator Register is Empty")
        return self.__value

    def __str__(self):
        return f"Accumulator: {self.get()}"


class PC:

    def __init__(self):
        self.__counter = 0

    def increment(self):
        self.__counter += 1

    def set(self, value: int):
        self.__counter = value

    def reset(self):
        self.__counter = 0

    def get(self):
        return self.__counter

    def __str__(self):
        return f"pc: {self.get()}"


class IR:

    def __init__(self):
        self.__instruction = ''
        self.__immediate = -sys.maxsize

    def is_empty(self):
        return self.__instruction == '' and self.__immediate == -sys.maxsize

    def set(self, instruction: str, immediate: int):
        IR.__check_instruction(instruction)
        self.__instruction = instruction
        self.__immediate = immediate

    def reset(self):
        self.__instruction = ''
        self.__immediate = -sys.maxsize

    def get_instruction(self):
        return self.__instruction

    def get_immediate(self):
        return self.__immediate

    @classmethod
    def __check_instruction(cls, instruction: str):
        ir_arr = ['load', 'add', 'sub', 'mul']

        if instruction not in ir_arr:
            raise Exception("Invalid Instruction")

    def __str__(self):
        return f"Instruction Register:{self.get_instruction()} {self.__immediate}"


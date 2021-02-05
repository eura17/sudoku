class Cell:
    def __init__(self, value: int = 0, sqr_size: int = 3):
        self.__value = value
        self.__sqr_size = sqr_size
        self.__possible_values = set() if value != 0 \
            else set(range(1, sqr_size ** 2+1))

    @property
    def value(self):
        return self.__value

    @property
    def possible_values(self):
        return self.__possible_values

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return f'Cell({self.__value}, {self.__sqr_size})'

    def __add__(self, other):
        if isinstance(other, Cell):
            return self.value + other.value
        elif isinstance(other, int):
            return self.value + other

    __radd__ = __add__

    def del_possible_value(self, value):
        if isinstance(value, int):
            self.__possible_values.discard(value)
        elif isinstance(value, set):
            self.__possible_values -= value

        if len(self.__possible_values) == 1:
            self.__value = self.__possible_values.pop()

    def is_correct(self):
        filled_right = len(self.__possible_values) == 0 and self.__value != 0
        unfilled_right = len(self.__possible_values) >= 1 and self.__value == 0
        return filled_right or unfilled_right

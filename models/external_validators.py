from os import stat


class IntegerHelpers:

    @staticmethod
    def is_even(value):
        if value % 2 != 0:
            raise ValueError(f"Value {value} is not even")
    
    @staticmethod
    def is_odd(value):
        if value % 2 == 0:
            raise ValueError(f"Value {value} should be odd")
    
    @staticmethod
    def is_positive(value):
        if value <= 0:
            raise ValueError(f"Value {value} should be positive")
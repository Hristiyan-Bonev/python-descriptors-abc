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


class StringHelpers:
    @staticmethod
    def is_in(value, values):
        if value not in values:
            raise ValueError(f"Value {value} not in {values!r}")

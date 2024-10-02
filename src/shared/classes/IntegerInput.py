from shared.classes.VariantsInput import VariantsInput
from typing import Tuple


class NumberBetweenInput(VariantsInput):
    @staticmethod
    def validate(value, options: Tuple[int, int]):
        if not isinstance(options, tuple) or len(options) != 2:
            raise TypeError("Options should be a tuple of two integers.")
        try:
            value = int(value)
        except ValueError:
            return False

        return options[0] <= value <= options[1]

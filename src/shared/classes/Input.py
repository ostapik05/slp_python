from typing import Tuple


class VariantsInput:
    @classmethod
    def input(cls, message, options=None, warning_message=None, is_finit=False):
        while True:
            value = input(message)
            if cls.validate(value, options):
                return value
            cls.in_wrong(warning_message or "Invalid input", value)
            if is_finit:
                break

    @classmethod
    def validate(cls, value, options=None):
        if not value:
            return False
        if options and value not in options:
            return False
        return True

    @classmethod
    def in_wrong(cls, value, message):
        print(f"{message} {value}")


class NumberBetweenInput(VariantsInput):

    @classmethod
    def validate(cls, value, options: Tuple[int, int]):
        if not isinstance(options, list) or len(options) != 2:
            raise TypeError("Options should be a list of two elements.")
        if not all(isinstance(x, int) for x in options):
            raise TypeError("Both elements in options should be integers.")
        try:
            value = int(value)
        except ValueError:
            return False

        return options[0] <= value <= options[1]


class BoolInput(VariantsInput):
    @classmethod
    def default(cls, message=None):
        if not message:
            message = "Choose (y/n)"
        true_options = ["y", "yes"]
        false_options = ["n", "no", "not"]
        input = cls.input(message, [true_options, false_options])
        return input

    @classmethod
    def input(cls, message, options=None, warning_message=None, is_finit=False):
        true_options = options[0]
        try:
            false_options = options[1]
        except:
            false_options = []
        while True:
            value = input(message)
            if cls.validate(value.lower(), true_options):
                return True
            if cls.validate(value.lower(), false_options):
                return False
            cls.in_wrong(warning_message or "Invalid input", value)
            if is_finit:
                return False


class StringInput(VariantsInput):

    @classmethod
    def input(
        cls,
        message,
        options=None | Tuple[int, int],
        warning_message=None,
        is_finit=False,
    ):
        no_limit = False
        try:
            lower_limit = options[0]
            upper_limit = options[1]
        except:
            no_limit = True
        while True:
            value = input(message)
            if no_limit:
                return value
            value_len = len(value)
            if NumberBetweenInput.validate(value_len, [lower_limit, upper_limit]):
                return value
            cls.in_wrong(warning_message or "Invalid lenght of value", value)
            if is_finit:
                break

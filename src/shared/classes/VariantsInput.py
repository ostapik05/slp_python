class VariantsInput:

    @staticmethod
    def input(message, options=None, warning_message=None, is_finit=False):
        while True:
            value = input(message)
            if VariantsInput.validate(value, options):
                return value
            VariantsInput.in_wrong(warning_message or "Invalid input", value)
            if is_finit:
                break

    @staticmethod
    def validate(value, options=None):
        if not value:
            return False
        if options and value not in options:
            return False
        return True

    @staticmethod
    def in_wrong(value, message):
        print(f"{message} {value}")

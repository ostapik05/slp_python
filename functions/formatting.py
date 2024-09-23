from functions.logger import log_error


def get_formatted_float(value, decimals, log_file):
    try:
        value = float(value)
        format = "{0:." + str(decimals) + "f}"
        return format.format(value)
    except ValueError as e:
        log_error(
            f"Неправильний тип значень {value} або {decimals}, повідомлення {e}",
            log_file,
        )
        return value

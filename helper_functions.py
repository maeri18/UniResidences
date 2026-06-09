import datetime
import logging


def date_to_formatted_str(date) -> str:
    return datetime.datetime.strftime(date, "%a_%d_%b_%Y-%H_%M_%S")


def start_logging(file_name_prefix: str, script_name: str):
    logger = logging.getLogger(script_name)

    date = date_to_formatted_str(datetime.datetime.now())
    filename = file_name_prefix + date + ".log"
    logging.basicConfig(filename=filename, encoding="utf-8", level=logging.DEBUG)

    return logger


def parse_bool_arg(argument: str):
    if argument is not None:
        if argument.lower() == "true":
            return True
        elif argument.lower() == "false":
            return False
    return None

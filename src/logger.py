import logging
import os
import traceback


class Logger:
    def __init__(self, log_file, clear=False):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        if clear and os.path.exists(log_file):
            open(log_file, "w").close()

        self.logger = logging.getLogger("GoodWeLogger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def exception(self, message: str, exc: Exception):
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        self.logger.error(f"{message}\n{tb}")

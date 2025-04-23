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
            "[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)

    def _get_logger_info(self):
        # Dynamically fetch the correct calling file and line number
        frame = logging.currentframe().f_back.f_back
        filename = os.path.basename(frame.f_globals["__file__"])
        lineno = frame.f_lineno
        return filename, lineno

    def info(self, message: str):
        filename, lineno = self._get_logger_info()
        self.logger.info(f"[{filename}:{lineno}] {message}")

    def warning(self, message: str):
        filename, lineno = self._get_logger_info()
        self.logger.warning(f"[{filename}:{lineno}] {message}")

    def error(self, message: str):
        filename, lineno = self._get_logger_info()
        self.logger.error(f"[{filename}:{lineno}] {message}")

    def exception(self, message: str, exc: Exception):
        filename, lineno = self._get_logger_info()
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        self.logger.error(f"[{filename}:{lineno}] {message}\n{tb}")

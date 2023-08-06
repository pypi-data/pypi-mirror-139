from logging import Logger
from rich.logging import RichHandler


class Logs(Logger):
    def __init__(self, level: str = "INFO", enable: bool = False):

        """
        Initialises standard logging module with RichHandler for richer and
        prettier logging.

        Args:
            enabled (bool): If set to true then level argument is taken
            into account, if false then logger is set to ERROR level.
            level (bool): logging level, possible options are:
                - "CRITICAL"
                - "ERROR"
                - "WARNING"
                - "INFO"
                - "DEBUG"
                more about logging levels in on this link:
                https://docs.python.org/3/howto/logging.html#logging-levels
        """
        super().__init__("rich")
        if enable:
            super().setLevel(level)
        else:
            super().setLevel("ERROR")

        super().addHandler(RichHandler(rich_tracebacks=True))

import logging


class LogManager:
    """
    The LogManager helps to manage the log pattern in all the modules in the EasyT project, and keep the same structure
    """
    def __init__(self, log_filename: str):
        """
        :param log_filename: str
            It holds the string name of the log file, it will be used to create the log file that will store the log.
            The log is overwritten everytime the script is called.
        """
        self.log_level = logging.INFO
        self.log_filename = log_filename

        self.string_log_format = '%(asctime)s %(levelname)s - %(funcName)s - %(message)s'

        # It handles the information that will be printed in the console that is equal or above a logging level
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.WARNING)
        self.console_handler.setFormatter(logging.Formatter(self.string_log_format))

        self.logger = logging

        # set the log configuration
        self.logger.basicConfig(level=self.log_level,
                                format=self.string_log_format,
                                filename=f'{self.log_filename}.log',
                                filemode='w'
                                )

        self.logger.getLogger().addHandler(self.console_handler)

    def debug(self, message: str):
        """
        Log level: 10, debug
        :param message: str
            It receives a debug message and stores it in the log file.
        :return: None
            It returns None and saves the log in the log file.
        """
        self.logger.debug(message)

    def info(self, message: str):
        """
        Log level: 20, info
        :param message: str
            It receives an info message and stores it in the log file.

        :return: None
            It returns None and saves the log in the log file.
        """
        self.logger.info(message)

    def warning(self, message: str):
        """
        Log level: 30, warning
        :param message: str
            It receives a warning message, print it into the console, and stores it in the log file.
        :return: None
            It returns None, print it into the console, and saves the log in the log file.
        """
        self.logger.warning(message)

    def error(self, message: str):
        """
        Log level: 40
        :param message: error
            It receives a error message, print it into the console, and stores it in the log file.
        :return: None
            It returns None, print it into the console, and saves the log in the log file.
        """
        self.logger.error(message)

    def critical(self, message: str):
        """
        Log level: 50
        :param message: critical
            It receives a critical message, print it into the console, and stores it in the log file.
        :return: None
            It returns None, print it into the console, and saves the log in the log file.
        """
        self.logger.critical(message)

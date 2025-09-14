import logging

class LoggerSetup:
    @staticmethod
    def initialize_logger(log_file='db_compare_app.log', log_level=logging.DEBUG):
        """
        Sets up logging with both console and file handlers.
        :param log_file: Path to the log file.
        :param log_level: Logging level (e.g., logging.INFO, logging.DEBUG).
        """
        logger = logging.getLogger()
        logger.setLevel(log_level)
        # Avoid adding handlers multiple times
        if not logger.handlers:
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            # File handler
            fh = logging.FileHandler(log_file)
            fh.setLevel(log_level)
            # Formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)
            # Add handlers
            logger.addHandler(ch)
            logger.addHandler(fh)
        return logger

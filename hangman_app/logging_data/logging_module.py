import logging
import os

# Define log directory
log_dir = os.path.join(os.path.dirname(__file__), "logging")
os.makedirs(log_dir, exist_ok=True)

# Define log file paths
game_report_log_file = os.path.join(log_dir, "game_report.log")
error_reporting_log_file = os.path.join(log_dir, "error_reporting.log")
game_logic_error_log_file = os.path.join(log_dir, "game_logic_error.log")
database_error_log_file = os.path.join(log_dir, "database_error.log")

game_report_logger = logging.getLogger("game_report_logger")
error_reporting_logger = logging.getLogger("error_reporting_logger")
game_logic_error_logger = logging.getLogger("game_logic_error_logger")
database_error_logger = logging.getLogger("database_error_logger")

game_report_logger.setLevel(logging.INFO)  # User activity logging (for reports :) )
error_reporting_logger.setLevel(logging.ERROR)  # Error logging
game_logic_error_logger.setLevel(logging.ERROR)  # Game logic error logging
database_error_logger.setLevel(logging.ERROR)  # Database error logging

game_report_handler = logging.FileHandler(game_report_log_file)
error_reporting_handler = logging.FileHandler(error_reporting_log_file)
game_logic_error_handler = logging.FileHandler(game_logic_error_log_file)
database_error_handler = logging.FileHandler(database_error_log_file)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

game_report_handler.setFormatter(formatter)
error_reporting_handler.setFormatter(formatter)
game_logic_error_handler.setFormatter(formatter)
database_error_handler.setFormatter(formatter)

game_report_logger.addHandler(game_report_handler)
error_reporting_logger.addHandler(error_reporting_handler)
game_logic_error_logger.addHandler(game_logic_error_handler)
database_error_logger.addHandler(database_error_handler)


def get_game_report_logger():
    return game_report_logger


def get_error_reporting_logger():
    return error_reporting_logger


def get_game_logic_error_logger():
    return game_logic_error_logger


def get_database_error_logger():
    return database_error_logger

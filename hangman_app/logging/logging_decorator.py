import logging
from functools import wraps

logging.basicConfig(
    level=logging.DEBUG,
    filename="game_data_logged.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)


# logging decorator that will try the function 3 times (can be adjusted), and logg the name of the funciton where error occurs
def log_decorator(retries=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if attempt == retries:
                        logging.error(
                            f"Error in function: {func.__name__} - {str(e)} (Attempt {attempt + 1}/{retries + 1})"
                        )
                        raise

        return wrapper

    return decorator

import logging


def log_settings():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename="app.log")

    return logging.getLogger(__name__)


logger = log_settings()


class FunctionExecutionError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self):
        return self.message


def log_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            message = f"Function: {func.__name__} args: {args} kwargs: {kwargs} result: {result}"
            logger.info(message)

            return result
        except Exception as e:
            message = f"Function: {func.__name__} args: {args} kwargs: {kwargs} exception: {e}"
            logger.error(message)
            raise FunctionExecutionError(message=message)

    return wrapper

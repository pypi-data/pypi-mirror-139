from rich.console import Console
from rich.text import Text
from datetime import datetime
from functools import wraps


def timeit(func):
    """Print cost time of `func` run."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        end = datetime.now()
        console = Console()
        text = Text.from_ansi("Cost time: \033[0;32m{0}\033[0m seconds".format(round((end - start).total_seconds(), 3)))
        console.print(text)

        return res
    return wrapper

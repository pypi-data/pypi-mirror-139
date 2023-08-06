"""Init."""
__version__ = "0.1.3"
from .model_pool import model_pool
from .fetch_check_aux import fetch_check_aux

from .model_s import load_model_s
from .load_model import load_model

__all__ = (
    "model_pool",
    "fetch_check_aux",
    "load_model_s",   # model_s = load_model_s()' model_s.encode(["a"])
    # "model_s",  # pyright pylint flake8 wont flag!
    "load_model",
)

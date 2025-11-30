from .dda_algorithm import dda_algorithm
from .bresenham_integer import bresenham_integer
from .slope_intercept_basic import slope_intercept_basic
from .slope_intercept_modified import slope_intercept_modified

ALGO_REGISTRY = {
    "slope_intercept_modified": slope_intercept_modified,
    "dda_algorithm": dda_algorithm,
    "bresenham_integer": bresenham_integer,
    "slope_intercept_basic": slope_intercept_basic,
}

__all__ = ["ALGO_REGISTRY"]
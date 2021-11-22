from functools import singledispatch, update_wrapper

# python 3.7 does not yet support singledispatchmethod
from typing import TypeVar, Callable, Optional

import numpy as np


def singledispatchmethod(func):
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


T = TypeVar('T')
S = TypeVar('S')


def optional_map(f: Callable[[T], S], x: Optional[T]) -> Optional[S]:
    return None if x is None else f(x)


def is_even(n: int) -> bool:
    return n % 2 == 0


def signed_permutation_inverse_2x2(matrix: np.ndarray):
    if matrix.shape != (2, 2):
        raise ValueError(f"Matrix have shape (2,2); found {matrix.shape}")
    det = matrix[0, 0] * matrix[1, 1] - matrix[1, 0] * matrix[0, 1]
    if np.abs(det) != 1:
        raise ValueError(f"Matrix must have determinant +/- 1; found {det}")
    return np.array([
        [matrix[1, 1], -matrix[0, 1]],
        [-matrix[1, 0], matrix[0, 0]]
    ], dtype=np.int) // det

from functools import singledispatch, update_wrapper


# python 3.7 does not yet support singledispatchmethod
import numpy as np


def singledispatchmethod(func):
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


def is_even(n: int) -> bool:
    return n % 2 == 0


def pixel_coord_to_pos(i, j, n):
    shift = n - 1 if is_even(n) else (n - 1)//2
    scale = 2 if is_even(n) else 1
    return j * scale - shift, i * scale - shift

def pos_to_pixel_coord(x, y, n):
    shift = n - 1 if is_even(n) else (n - 1) // 2
    scale = 2 if is_even(n) else 1
    return (y + shift) // scale, (x + shift) // scale

def transform_pixels(transform, pixels):
    n = pixels.shape[0]
    transformed_index = np.array(
        [
            np.ravel_multi_index(
                pos_to_pixel_coord(
                    *np.dot(transform, np.array(pixel_coord_to_pos(*np.unravel_index(idx, pixels.shape), n))),
                    n
                ), pixels.shape
            )
            for idx in range(n * n)]
    )
    return pixels.ravel()[transformed_index].reshape(pixels.shape)
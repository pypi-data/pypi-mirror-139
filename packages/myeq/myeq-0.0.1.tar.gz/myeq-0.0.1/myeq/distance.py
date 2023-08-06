from math import e


def inv_norm_sigmoid(x: float, s: float = 0.3, t: float = 0.88, b: float = 0, p: float = 3.3) -> float:
    """ Approach a value to a inverse normalized sigmoid function which starts in 0 with a value of 1,
    and it is reducing until the limit 0 in the infinite.

       You can test this function in `demos web page <https://www.desmos.com/calculator/qmgr2zwa4b>`_.

    :param x: The value to normalize.
    :param s: The velocity of decreasing function.
    :param t: The bottom limit velocity.
    :param b: The upper limit (0 for 1, and 1 for 0)
    :param p: The curve with.
    :return: A value between 0 and 1 with the value x normalized by an inverse sigmoid.
    """
    return 1 - (b + (t - b) / (1 + e **((p - abs(x)) / s)))

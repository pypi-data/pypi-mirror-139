"""Computational processing related to image processing."""

from typing import Tuple


def _calc_internally(p1: float, p2: float, ratio: Tuple[float, float]) -> float:
    """Calculate the point that divides internally.

    Args:
        p1 (float): point 1
        p2 (float): point 2
        ratio (float): ratio of division

    Returns:
        float: divided point
    """
    num_ratio = ratio[0] / (ratio[0] + ratio[1])
    assert 0 <= num_ratio <= 1
    if p1 < p2:
        dist = p2 - p1
        return p1 + dist * num_ratio
    else:
        dist = p1 - p2
        return p1 - dist * num_ratio


def divide_internally(p1: Tuple[int, int], p2: Tuple[int, int], ratio: Tuple[float, float]) -> Tuple[int, int]:
    """Obtain internally division point.

    obtain the point that divides internally

    Args:
        p1 (Tuple[int, int]): point 1
        p2 (Tuple[int, int]): point 2
        ratio (float): ratio of division

    Returns:
        Tuple[int, int]: divided point

    """
    x = _calc_internally(p1[0], p2[0], ratio)
    y = _calc_internally(p1[1], p2[1], ratio)

    return (int(x), int(y))


def _calc_externally(p1: float, p2: float, ratio: Tuple[float, float]) -> float:
    """Calculate the point that divides externally.

    Args:
        p1 (float): point 1
        p2 (float): point 2
        ratio (float): rate of division

    Returns:
        float: divided point
    """
    if ratio[0] >= ratio[1]:
        num_ratio = ratio[0] / (ratio[0] - ratio[1])
        assert num_ratio >= 1
        if p1 < p2:
            dist = p2 - p1
            return p1 + dist * num_ratio
        else:
            dist = p1 - p2
            return p2 + dist * num_ratio
    else:
        num_ratio = ratio[1] / (ratio[1] - ratio[0])
        assert num_ratio >= 1
        if p1 < p2:
            dist = p2 - p1
            return p1 + dist * num_ratio
        else:
            dist = p1 - p2
            return p2 + dist * num_ratio


def divide_externally(p1: Tuple[int, int], p2: Tuple[int, int], ratio: Tuple[float, float]) -> Tuple[int, int]:
    """Obtain externally division point.

    obtain the point that divides internally

    Args:
        p1 (Tuple[int, int]): point 1
        p2 (Tuple[int, int]): point 2
        ratio (float): ratio of division

    Returns:
        Tuple[int, int]: divided point

    """
    x = _calc_externally(p1[0], p2[0], ratio)
    y = _calc_externally(p1[1], p2[1], ratio)

    return (int(x), int(y))

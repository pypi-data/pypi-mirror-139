import pytest
from hw1.src.hw1_package.fibonacci import get_n_fibonacci_number


def test_fibonacci(sequence):
    """
    Test checks that first 10 fibonacci numbers are computed correctly.
    """
    key, value = sequence
    assert value == get_n_fibonacci_number(key)


@pytest.fixture(params=[(1, 0), (2, 1), (3, 1), (4, 2), (5, 3), (6, 5), (7, 8), (8, 13), (9, 21), (10, 34)])
def sequence(request):
    """
    Consistently yields 10 tuples of numbers (fibonacci sequence number and fibonacci number).
    """
    yield request.param


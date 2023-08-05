def get_n_fibonacci_number(n: int):
    """
    Simple version of fibonacci number calculations, with cashing.
    :param n: int number of fibonacci sequences to return.
    :return: int n'th fibonacci number.
    """
    first_fibonacci_number = 0
    second_fibonacci_number = 1

    if n == 1:
        return first_fibonacci_number

    elif n == 2:
        return second_fibonacci_number

    elif n < 1:
        raise AssertionError("Function takes only positive integers.")

    else:
        for i in range(n - 2):
            to_become_first = second_fibonacci_number
            second_fibonacci_number = first_fibonacci_number + second_fibonacci_number
            first_fibonacci_number = to_become_first
        return second_fibonacci_number

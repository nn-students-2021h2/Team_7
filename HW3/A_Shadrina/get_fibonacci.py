# наивное рекурсивное решение, для проверки нагрузки на ЦП
def get_fibonacci_value(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return get_fibonacci_value(n - 1) + get_fibonacci_value(n - 2)

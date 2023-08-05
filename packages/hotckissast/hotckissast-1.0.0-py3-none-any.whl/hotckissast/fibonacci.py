def fib(n):
    result = [0, 1]
    for _ in range(n - 2):
        result.append(result[-1] + result[-2])
    return result
def fib(n : int):
    if n < 1:
        return []
    if n == 1:
        return [0]
    numbers = [0, 1]
    for i in range(n-2):
        numbers.append(numbers[-1] + numbers[-2])
    return numbers
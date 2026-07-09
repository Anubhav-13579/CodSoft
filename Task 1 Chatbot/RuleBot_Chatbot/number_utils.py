import math

def is_even_or_odd(num):
    return "Even" if num % 2 == 0 else "Odd"

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def is_armstrong(num):
    if num < 0:
        return False
    digits = str(num)
    length = len(digits)
    total = sum(int(digit) ** length for digit in digits)
    return total == num

def fibonacci_series(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    series = [0, 1]
    while len(series) < n:
        series.append(series[-1] + series[-2])
    return series

def factorial(n):
    if n < 0:
        return None
    return math.factorial(n)

def largest_of_two(a, b):
    return a if a > b else b

def largest_of_three(a, b, c):
    return max(a, b, c)

def calculate_lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def calculate_gcd(a, b):
    return math.gcd(a, b)

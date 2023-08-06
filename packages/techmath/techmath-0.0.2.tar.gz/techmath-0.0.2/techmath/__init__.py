

#  Fibonacci number
def fib_num(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b


# Factorial number
a = 1
def fact_num(n):
    global a
    for i in range(1, n+1):
        a = a*i
    print(a)

# square root of number


def sqrr_num(n):
    x = n**0.5
    print(x)

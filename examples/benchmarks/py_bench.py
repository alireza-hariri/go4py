import random
import requests
import numpy as np
from examples.benchmarks import add, rand, randn, randArray, getRequest, fibo, findPrimes

import timeit


def Rand_py() -> float:
    return random.random()


def Randn_py() -> float:
    return random.normalvariate(0, 1)


def Add_py(a):
    return a + 10_000


def RandArray_py(n: int) -> list[float]:
    return [random.random() for _ in range(n)]


def RandArray_numpy(n: int) -> list[float]:
    return np.random.rand(n).tolist()


def GetRequest_py(url: str) -> tuple[bytes, str]:
    requests.get(url)


# export Fibo_py
def Fibo_py(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b


# export FindPrimes_py
def FindPrimes_py(n: int) -> list[int]:
    primes = []
    for i in range(2, n):
        isPrime = True
        for j in range(2, i):
            if i % j == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(i)
    return primes


pairs = [
    (rand, Rand_py),
    (randn, Randn_py),
]


for go_fn, py_fn in pairs:
    print(go_fn.__name__, py_fn.__name__)
    t1 = timeit.timeit(go_fn, number=100000)
    t2 = timeit.timeit(py_fn, number=100000)
    print(f"go4py speedup {t2 / t1:.1f}x\n")


pairs = [
    (add, Add_py),
    (randArray, RandArray_py),
    (randArray, RandArray_numpy),
    (fibo, Fibo_py),
    (findPrimes, FindPrimes_py),
]


arg = 10, 20, 40, 80

for a in arg:
    for go_fn, py_fn in pairs:
        print(py_fn.__name__, f"a={a}")
        t1 = timeit.timeit(lambda: go_fn(a), number=10000)
        t2 = timeit.timeit(lambda: py_fn(a), number=10000)
        print(f"go4py speedup {t2 / t1:.1f}x\n")


pairs = [
    (getRequest, GetRequest_py),
]
url = "http://localhost:8080/hello"

for go_fn, py_fn in pairs:
    print(go_fn.__name__, py_fn.__name__)
    t1 = timeit.timeit(lambda: go_fn(url), number=1000)
    t2 = timeit.timeit(lambda: py_fn(url), number=1000)
    print(f"go4py speedup {t2 / t1:.1f}x")

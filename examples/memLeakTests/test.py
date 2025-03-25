import random

from examples.memLeakTests import func_x, func_5, func_6, func_7, func_8, func_10, func_11

from examples.memLeakTests import func_1, func_2, func_3, func_4, func_5_2

%%timeit
for i in range(100_000):
    a = [random.randint(0,10) for _ in range(10)]
    func_1(a)

%%timeit
for i in range(10_000):
    a = "1"*random.randint(0,1000)+"2"
    func_2([a],[a])

%%timeit 
func_3()

%%timeit
func_4()

%%timeit
func_5_2()

%%timeit
func_7("1", 1, "2", 3.0)
import time

from z3 import *


def get_if_arr(arr, index, length):
    if index == 10:
        return arr[0]

    return If(get_and_arr(arr, index, length), arr[index], get_if_arr(arr, index + 1, length))


def get_and_arr(arr, index, length):
    constraints = []
    for i in range(10):
        and_constraint = Implies(i < length, arr[index] <= arr[i])
        constraints.append(and_constraint)
    return And(index < length, *constraints)


s = Solver()

length = Int('length')
arr = Array('arr', IntSort(), IntSort())
min_arr = Int('min_arr')

# Solution:

# i = Int('i')
# j = Int('j')
# f = ForAll([i, j], Implies(And(i >= 0, i < length, j >= i, j < 5), min_arr <= arr[i]))
# s.add(f)
#
# e = Exists([i], And(i >= 0, i < length, min_arr == arr[i]))
# s.add(e)
#
# s.add(length == 5)
# s.add(min_arr == 2)
#
# s.add(arr[2] == 2)

# Sum solution:

i = Int('i')

s.add(length == 5)
# s.add(Sum([i], And(i >= 0, i < length, arr[i] == 2)) == 1)

# f = Function('f', IntSort(), IntSort())
# s.add(f(0) == 1)

# sumArray = Function('sumArray', IntSort(), IntSort())
# s.add(sumArray(-1) == 0)
# i = Int('i')
# s.add(ForAll([i], Implies(And(i >= 0, i < 5), sumArray(i) == sumArray(i - 1) + arr[i])))
#
# sumResult = Int('sumResult')
# s.add(sumResult == sumArray(length - 1))

#
# i = If(length == 2, (arr[0], arr[1]), arr[3])
#
# #z3.is_lt()
#
#
# index = Int('index')
# min_arr = Int('min_arr')
# if_arr = get_if_arr(arr, 0, length)
#
# s.add(length == 5)
# s.add(min_arr == if_arr)
#
# # e = Exists([index], And([index < length, arr[index] == min_arr]))
# # s.add(e)
#
# s.add(min_arr == 2)
# s.add(arr[0] != 2)
# # s.add(arr[0] == 8)
# # s.add(arr[1] == 6)
# # s.add(arr[3] == 4)


print(s.check())
m = s.model()
arr_str = ",".join([f"{m.evaluate(arr[i]).as_long()}" for i in range(5)])
print(f"arr: {arr_str}")
# print(f"length: {m.evaluate(length).as_long()}")
# print(f"min_arr: {m.evaluate(min_arr).as_long()}")
print(f"sumResult: {m.evaluate(sumResult).as_long()}")

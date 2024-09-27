import time

from z3 import *

arr_1 = Array('a', IntSort(), IntSort())
arr_2 = Array('b', IntSort(), IntSort())

a_length = Int('a_length')
b_length = Int('b_length')

a_index = Int("a_index")
b_index = Int("b_index")

a_is_null = Bool('a_is_null')
b_is_null = Bool('b_is_null')

s = Solver()

is_null = Bool('is_null')
s.add(is_null == True)

# s.add(a_length >= 0)
# s.add(ForAll(a_index, arr_1[a_index] >= -2147483647))
# s.add(ForAll(a_index, arr_1[a_index] <= 2147483647))
# s.add(a_length >= -2147483647)
# s.add(a_length <= 2147483647)
# s.add(b_length >= 0)
# s.add(ForAll(b_index, arr_2[b_index] >= -2147483647))
# s.add(ForAll(b_index, arr_2[b_index] <= 2147483647))
# s.add(b_length >= -2147483647)
# s.add(b_length <= 2147483647)
# s.add(And(a_is_null != is_null, b_is_null != is_null))

s.push()

a_new_index = Int("a_index")
b_new_index = Int("b_index")

# and_expr = And(
#     And(ForAll(a_new_index, arr_1[a_index] == 1), a_length == 1),
#     And(ForAll(a_new_index, arr_2[a_new_index] == 1), b_length == 1)
# )
# s.add(and_expr)

# s.add(And(ForAll(a_index, And(arr_1[a_index] == 1)), a_length == 1))
#

s.add(ForAll(a_index, Implies(And(a_index >= 0, a_index < 100), arr_1[a_index] == 1)))
s.add(ForAll(a_new_index, Implies(And(a_new_index >= 0, a_new_index < 100), arr_2[a_new_index] == 1)))

start_time = time.time()

if s.check() == sat:
    print(s.model())
else:
    print("Unsat")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time}")

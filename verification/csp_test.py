from z3 import *

# (\forall int i,j; 0 <= i && i < j && j < 10; a[i] < a[j])

i = Int('i')
j = Int('j')

s = Solver()
s.add(And(And(i >= 0, i < j), j < 10))

print(s.check())
m = s.model()
print(f"arr: {m}")
# print(f"length: {m.evaluate(length).as_long()}")
# print(f"min_arr: {m.evaluate(min_arr).as_long()}")
# print(f"sumResult: {m.evaluate(sumResult).as_long()}")

from z3 import *

# Erstellen eines Arrays von IntSort (Integer-Werten)
arr = Int('arr')
b = Bool("None")

# Erstellen eines Z3-Solvers
solver = Solver()

#solver.add(ForAll(index, arr[index] > -200000))
solver.add(arr == Empty)

# Überprüfen, ob es eine Lösung gibt
if solver.check() == sat:
    model = solver.model()
    print("Lösung gefunden")
else:
    print("Keine Lösung gefunden")

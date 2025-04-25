from z3 import ArraySort, Array, IntSort, Solver, sat

I = Array('I', IntSort(), IntSort())
O = Array('I', IntSort(), IntSort())

solver = Solver()
solver.add(I[0] == 1)

if solver.check() == sat:
    model = solver.model()
    print(model)

    params = list(model)
    print(params)

    print(model.evaluate(I[10]))

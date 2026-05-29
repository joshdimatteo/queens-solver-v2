import puzzle
import solver
from time import sleep

# Create blank puzzle
p = puzzle.Puzzle(12, 0.05)
s = solver.Solver(p)

# Build and mark it
p.build((690, 335), (1205, 850))

print("Colors:")
print(p.colors)

s.solve()

print()
print(p.marks)

# Bounds:
# Top Left: (690, 335)
# Bottom Right: (1205, 850)
# p.build((690, 335), (1205, 850))
p.apply((690, 335), (1205, 850))

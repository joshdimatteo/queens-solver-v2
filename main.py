import puzzle
import solver
from time import sleep

# Create blank puzzle
p = puzzle.Puzzle(5)
s = solver.Solver(p)

# Build and mark it
# p.build((690, 335), (1205, 850))

p.mark((0, 0), 1)
p.mark((1, 0), 1)
p.mark((2, 0), 1)
print("Marks:")
print(p.marks, end="\n\n")

s.mark_line_search()

print()
print()
print(p.marks)

# Bounds:
# Top Left: (690, 335)
# Bottom Right: (1205, 850)
# p.build((690, 335), (1205, 850))
# p.apply((690, 335), (1205, 850))

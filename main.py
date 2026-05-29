import puzzle
from time import sleep

# Create blank puzzle
p = puzzle.Puzzle(5)
print(p.marks, end="\n\n")

# Build and mark it
p.build((690, 335), (1205, 850))

print(p.colors, end="\n\n")

p.mark((1, 0), 2)
p.mark((4, 1), 2)
p.mark((3, 4), 2)
p.mark((0, 3), 2)
p.mark((2, 2), 2)
print(p.marks, end="\n\n")
print(p.is_solved())
print(p.is_valid())

# Bounds:
# Top Left: (690, 335)
# Bottom Right: (1205, 850)
# p.build((690, 335), (1205, 850))
# p.apply((690, 335), (1205, 850))

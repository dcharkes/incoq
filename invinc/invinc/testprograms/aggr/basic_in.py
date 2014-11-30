# Basic aggregate query.

from runtimelib import *

OPTIONS(
    default_impl = 'inc',
)

R = Set()

for x in [1, 2, 3, 4, 5]:
    R.add(x)

R.remove(5)

print(sum(R))

for x in [1, 2, 3, 4]:
    R.remove(x)

print(sum(R))

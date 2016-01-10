# Nested comprehensions.

from incoq.mars.runtime import *

SYMCONFIG('Q1',
    impl = 'inc',
)
SYMCONFIG('Q2',
    impl = 'inc',
)

S = Set()

def main():
    for x, y in [(1, 1), (1, 2), (2, 2), (2, 3)]:
        S.add((x, y))
    print(QUERY('Q2', {v for (v,) in QUERY('Q1', {(a,) for (a, b) in S
                                                       if a == b})
                        if v > 1}))

if __name__ == '__main__':
    main()

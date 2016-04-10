# Q1 : a -> {(a, b) for (a, b) in REL(S)} : {(Number, Number)}
# Q2 : a -> sum(unwrap(R_Q1.imglookup('bu', (a,)))) : Top
from incoq.mars.runtime import *
# S : {(Number, Number)}
S = Set()
# R_Q1 : {(Number, Number)}
R_Q1 = Set()
# A_Q2 : {(Number): Number}
A_Q2 = Map()
def _maint_A_Q2_for_R_Q1_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v5_key = (_elem_v1,)
    _v5_value = _elem_v2
    _v5_state = A_Q2.get(_v5_key, (0, 0))
    _v5_state = ((index(_v5_state, 0) + _v5_value), (index(_v5_state, 1) + 1))
    if (_v5_key in A_Q2):
        del A_Q2[_v5_key]
    A_Q2[_v5_key] = _v5_state

def _maint_A_Q2_for_R_Q1_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v6_key = (_elem_v1,)
    _v6_value = _elem_v2
    _v6_state = A_Q2[_v6_key]
    _v6_state = ((index(_v6_state, 0) - _v6_value), (index(_v6_state, 1) - 1))
    del A_Q2[_v6_key]
    if (not (index(_v6_state, 1) == 0)):
        A_Q2[_v6_key] = _v6_state

def _maint_R_Q1_for_S_add(_elem):
    (_v3_a, _v3_b) = _elem
    _v3_result = (_v3_a, _v3_b)
    R_Q1.add(_v3_result)
    _maint_A_Q2_for_R_Q1_add(_v3_result)

def _maint_R_Q1_for_S_remove(_elem):
    (_v4_a, _v4_b) = _elem
    _v4_result = (_v4_a, _v4_b)
    _maint_A_Q2_for_R_Q1_remove(_v4_result)
    R_Q1.remove(_v4_result)

def main():
    for (x, y) in [(1, 2), (2, 3), (2, 4), (3, 4)]:
        _v1 = (x, y)
        S.add(_v1)
        _maint_R_Q1_for_S_add(_v1)
    a = 1
    print(index(A_Q2.get((a,), (0, 0)), 0))
    a = 0
    print(index(A_Q2.get((a,), (0, 0)), 0))
    a = 2
    print(index(A_Q2.get((a,), (0, 0)), 0))
    _v2 = (2, 4)
    _maint_R_Q1_for_S_remove(_v2)
    S.remove(_v2)
    print(index(A_Q2.get((a,), (0, 0)), 0))
    A_Q2.dictclear()
    R_Q1.clear()
    S.clear()
    print(index(A_Q2.get((a,), (0, 0)), 0))

if (__name__ == '__main__'):
    main()